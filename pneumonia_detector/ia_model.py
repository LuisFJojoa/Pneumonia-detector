import numpy as np


class ModelStrategy:

    def __init__(self, grad_cam, image_procesor, model):
        self.grad_cam = grad_cam
        self.image_procesor = image_procesor
        self.model = model

    def predict(self, array): 
        batch_array_img = self.image_procesor.preprocess(array)
        # call function to load model and predict: it returns predicted class and probability
        prediction = np.argmax(self.model.predict(batch_array_img))
        proba = np.max(self.model.predict(batch_array_img)) * 100
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
    
