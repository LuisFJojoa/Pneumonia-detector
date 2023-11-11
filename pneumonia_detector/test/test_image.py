import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from image import ImageLoader


def test_valid_image_formats():

    image_loader = ImageLoader()

    valid_jpeg_path = "../../volumes/Images/JPG/bacteria/person1710_bacteria_4526.jpeg"
    valid_dicom_path = "../../volumes/Images/DICOM/normal (2).dcm"

    invalid_path = "../../volumes/Images/OTHER_FORMAT/test.png"

    assert image_loader.is_supported_format(valid_jpeg_path) is True
    assert image_loader.is_supported_format(valid_dicom_path) is True

    assert image_loader.is_supported_format(invalid_path) is False
