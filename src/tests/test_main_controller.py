"""Testing the main controller"""
from os.path import dirname
from models import main_model
from controllers import main_controller


def test_main_controller(qtbot):  # pylint: disable=W0613
    # WARNING: qtbot is required as an argument even though it is
    # never used because a GUI instance is created as an outcome
    # of the below tests I believe
    """
    Testing the main controller
    """
    model = main_model.MainModel()
    controller = main_controller.MainController(model)

    controller.change_selected_dicom_directory("dicom_file")
    # assert model.selected_dicom_directory == "dicom_file"

    # returns a list of 1 file
    assert len(controller.get_dicom_image_files_in_selected_path()) == 1
    assert controller.get_config() is not None

    # it is null until we call controller.change_selected_image_file_path()
    assert controller.get_dicom_image_parser() is None

    parent_directory = dirname(__file__).split("\\src")[0]
    image_path = f"{parent_directory}\\dicom_file\\CT_183_Hashed.dcm"
    controller.change_selected_image_file_path(image_path)

    controller.get_next_image_file_path()
    controller.get_previous_image_file_path()
