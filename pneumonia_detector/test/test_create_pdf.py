import sys
import os
import tensorflow as tf

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gui import GUI 
from grad_cam import GradCAM 
from image import ImageLoader, ImageProcessor
from app import App
from ia_model import ModelStrategy


def test_create_pdf():
    model = tf.keras.models.load_model('conv_MLP_84.h5')
    image_loader = ImageLoader()
    image_processor = ImageProcessor()
    grad_cam = GradCAM(image_processor, model)
    model_strategy = ModelStrategy(grad_cam, image_processor, model)
    my_app = App(image_processor, model_strategy, grad_cam)
    gui = GUI(my_app, image_loader)

    gui.personal_id_text.insert(0, "12345678")

    pdf_path = my_app.create_pdf(gui.root, gui.personal_id_text.get())

    assert os.path.exists(pdf_path), "PDF File wasn't created correctly"

    assert pdf_path.endswith('.pdf'), "PDF File was created correctly"
