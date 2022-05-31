"""Testing the image window"""
from os.path import dirname
from models import main_model
from controllers import main_controller


def test_image_window(qtbot):
    """
    Testing the image window view
    """
    model = main_model.MainModel()
    controller = main_controller.MainController(model)

    parent_directory = dirname(__file__).split("\\src")[0]

    # WARNING: this path will probably only work on windows?
    # calling this will trigger the image window to be instantiated/tested
    image_path = f"{parent_directory}\\dicom_file\\CT_183_Hashed.dcm"
    controller.change_selected_image_file_path(image_path)

    qtbot.addWidget(controller.dicom_image_window)

    # try scroll here?
