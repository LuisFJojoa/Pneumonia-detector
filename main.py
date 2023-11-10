#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tensorflow as tf

from gui import GUI 
from grad_cam import GradCAM 
from image import ImageLoader, ImageProcessor
from app import App
from ia_model import ModelStrategy


def main():
    model = tf.keras.models.load_model('conv_MLP_84.h5')
    image_loader = ImageLoader()
    image_processor = ImageProcessor()
    grad_cam = GradCAM(image_processor, model)
    model_strategy = ModelStrategy(grad_cam, image_processor, model) 
    my_app = App(image_processor, model_strategy, grad_cam)
    gui = GUI(my_app, image_loader)
    gui.run()
    return 0


if __name__ == "__main__":
    main()
