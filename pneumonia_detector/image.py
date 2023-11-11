import os
import cv2
import pydicom
import numpy as np

from PIL import Image


class ImageLoader:
    SUPPORTED_FORMATS = (".jpg", ".jpeg", ".dcm")

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

    def is_supported_format(self, file_path):
        _, file_extension = os.path.splitext(file_path)
        return file_extension.lower() in self.SUPPORTED_FORMATS


class DICOMReader:
    def read(self, path):
        img = pydicom.dcmread(path)
        img_array = img.pixel_array
        img_from_array = Image.fromarray(img_array)
        new_image = img_array.astype(float)
        new_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0
        new_image = np.uint8(new_image)
        img_RGB = cv2.cvtColor(new_image, cv2.COLOR_GRAY2RGB)
        return img_RGB, img_from_array


class JPGImageReader:
    def read(self, path):
        img = cv2.imread(path)
        img_array = np.asarray(img)
        img_from_array = Image.fromarray(img_array)
        new_image = img_array.astype(float)
        new_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0
        new_image = np.uint8(new_image)
        return new_image, img_from_array


class ImageProcessor:
    def preprocess(self, array):
        array = cv2.resize(array, (512, 512))
        array = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
        array = clahe.apply(array)
        array = array / 255
        array = np.expand_dims(array, axis=-1)
        array = np.expand_dims(array, axis=0)
        return array
