#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import tensorflow as tf


from keras import backend as K


tf.compat.v1.disable_eager_execution()
tf.compat.v1.experimental.output_all_intermediates(True)


class GradCAM:

    def __init__(self, image_processor):
        self.image_processor = image_processor

    def generate_heatmap(self, array):
        img = self.image_processor.preprocess(array)
        model = tf.keras.models.load_model('../conv_MLP_84.h5')
        preds = model.predict(img)
        argmax = np.argmax(preds[0])
        output = model.output[:, argmax]
        last_conv_layer = model.get_layer("conv10_thisone")
        grads = K.gradients(output, last_conv_layer.output)[0]
        pooled_grads = K.mean(grads, axis=(0, 1, 2))
        iterate = K.function([model.input], [pooled_grads, last_conv_layer.output[0]])
        pooled_grads_value, conv_layer_output_value = iterate(img)
        for filters in range(64):
            conv_layer_output_value[:, :, filters] *= pooled_grads_value[filters]
        # creating the heatmap
        heatmap = np.mean(conv_layer_output_value, axis=-1)
        heatmap = np.maximum(heatmap, 0)  # ReLU
        heatmap /= np.max(heatmap)  # normalize
        heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[2]))
        superimposed_img = self.overlay_heatmap(heatmap, array)
        return superimposed_img 

    def overlay_heatmap(self, heatmap, array, alpha=0.8):
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        img2 = cv2.resize(array, (512, 512))
        hif = 0.8
        transparency = heatmap * hif
        transparency = transparency.astype(np.uint8)
        superimposed_img = cv2.add(transparency, img2)
        superimposed_img = superimposed_img.astype(np.uint8)
        return superimposed_img[:, :, ::-1]
