#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import os
import getpass
import pydicom
import csv
import pyautogui
import tkcap
import img2pdf
import numpy as np
import time
import tensorflow as tf

from tkinter import *
from tkinter import ttk, font, filedialog, Entry

from keras import backend as K
from tkinter.messagebox import askokcancel, showinfo, WARNING
from PIL import ImageTk, Image

from gui import GUI 

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


class ModelStrategy:

    def __init__(self, grad_cam):
        self.grad_cam = grad_cam

    def predict(self, array): 
        batch_array_img = ImageProcessor().preprocess(array)
        # call function to load model and predict: it returns predicted class and probability
        model = tf.keras.models.load_model('../conv_MLP_84.h5')
        prediction = np.argmax(model.predict(batch_array_img))
        proba = np.max(model.predict(batch_array_img)) * 100
        label = ""
        if prediction == 0:
            label = "bacteriana"
        if prediction == 1:
            label = "normal"
        if prediction == 2:
            label = "viral"
        # call function to generate Grad-CAM: it returns an image with a superimposed heatmap
        heatmap = self.grad_cam.generate_heatmap(array)
        return (label, proba, heatmap)


class ImageLoader:
    @staticmethod
    def load_image(path):
        _, ext = path.rsplit('.', 1)
        ext = ext.lower()

        if ext == 'dcm':
            return DICOMReader().read(path)
        elif ext == 'jpg' or ext == 'jpeg':
            return JPGImageReader().read(path)
        else:
            raise ValueError("Unsupported image format")


class DICOMReader:
    def read(self, path):
        img = pydicom.dcmread(path)
        img_array = img.pixel_array
        img2show = Image.fromarray(img_array)
        img2 = img_array.astype(float)
        img2 = (np.maximum(img2, 0) / img2.max()) * 255.0
        img2 = np.uint8(img2)
        img_RGB = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB)
        return img_RGB, img2show


class JPGImageReader:
    def read(self, path):
        img = cv2.imread(path)
        img_array = np.asarray(img)
        img2show = Image.fromarray(img_array)
        img2 = img_array.astype(float)
        img2 = (np.maximum(img2, 0) / img2.max()) * 255.0
        img2 = np.uint8(img2)
        return img2, img2show


class ImageProcessor:
    def preprocess(self, array):
        # Implementa el preprocesamiento de imágenes
        array = cv2.resize(array, (512, 512))
        array = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
        array = clahe.apply(array)
        array = array / 255
        array = np.expand_dims(array, axis=-1)
        array = np.expand_dims(array, axis=0)
        return array


class App:
    def __init__(self, image_processor, model_strategy, grad_cam):
        self.image_processor = image_processor
        self.model_strategy = model_strategy
        self.grad_cam = grad_cam

    #   METHODS
    def preprocess_image(self, array):
        processed_array = self.image_processor.preprocess(array)
        return processed_array

    def run_model(self, gui):
        self.label, self.proba, self.heatmap = self.model_strategy.predict(gui.array)
        gui.img2 = Image.fromarray(self.heatmap)
        gui.img2 = gui.img2.resize((250, 250), Image.LANCZOS)
        gui.img2 = ImageTk.PhotoImage(gui.img2)
        print("OK")
        gui.text_img2.image_create(END, image=gui.img2)
        gui.text2.insert(END, self.label)
        gui.text3.insert(END, "{:.2f}".format(self.proba) + "%")
    
    def save_results_csv(self):
        with open("historial.csv", "a") as csvfile:
            w = csv.writer(csvfile, delimiter="-")
            w.writerow(
                [self.text1.get(), self.label, "{:.2f}".format(self.proba) + "%"]
            )
            showinfo(title="Guardar", message="Los datos se guardaron con éxito.")

    def create_pdf(self):
        cap = tkcap.CAP(self.root)
        ID = "Reporte" + str(self.reportID) + ".jpg"
        img = cap.capture(ID)
        img = Image.open(ID)
        img = img.convert("RGB")
        pdf_path = r"Reporte" + str(self.reportID) + ".pdf"
        img.save(pdf_path)
        self.reportID += 1
        showinfo(title="PDF", message="El PDF fue generado con éxito.")


def main():
    image_loader = ImageLoader()
    image_processor = ImageProcessor()
    grad_cam = GradCAM(image_processor)
    model_strategy = ModelStrategy(grad_cam) 
    my_app = App(image_processor, model_strategy, grad_cam)
    gui = GUI(my_app, image_loader)
    gui.run()
    return 0


if __name__ == "__main__":
    main()
