"""Testing the main model"""
from models import main_model


def test_main_model():
    """
    Creates a MainModel instance and tests it's functions
    """
    model = main_model.MainModel()

    # uses setter methods
    model.selected_dicom_directory = "new_dicom_directory"
    model.selected_image_file_path = "new_image_file_path"

    # tests getter methods
    assert model.selected_dicom_directory == "new_dicom_directory"
    assert model.selected_image_file_path == "new_image_file_path"
