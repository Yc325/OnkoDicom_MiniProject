"""
Instantiating some classes
"""
# import pytest
# from pytestqt.plugin import QtBot
from models import dicom_file_parser_model
from models import main_model
from controllers import main_controller
# from views.main_window import MainView
# from views.popup_for_default_directory import Popup


def test_main_model():
    """
    Creates a MainModel instance
    """
    model = main_model.MainModel()

    # uses setter methods
    model.selected_dicom_directory = "new_dicom_directory"
    model.selected_image_file_path = "new_image_file_path"

    # tests getter methods
    assert model.selected_dicom_directory == "new_dicom_directory"
    assert model.selected_image_file_path == "new_image_file_path"


def test_dicom_file_parser_model():
    """
    Creates a DicomFileParserModel instance
    """

    # WARNING: changing this example file will cause this test to fail
    example_dicom_image_path = "dicom_file/CT_183_Hashed.dcm"
    model = dicom_file_parser_model.DicomFileModel(example_dicom_image_path)

    assert model.get_instance_number() == 183
    assert model.get_qtimage() is not None
    assert model.get_type() == "CT Image"
    assert model.get_body_part_title() == "NECK"


def test_main_controller():
    """
    Testing the main controller
    """
    model = main_model.MainModel()
    controller = main_controller.MainController(model)

    controller.change_selected_dicom_directory("test/test")
    assert model.selected_dicom_directory == "test/test"

    # returns a list of 1 file
    assert len(controller.get_dicom_image_files_in_selected_path(
        "dicom_file")) == 1
    assert controller.get_config() is not None


# @pytest.fixture
# def qtbot(request):
#     """
#     Fixture used to create a QtBot instance for using during testing.

#     Make sure to call addWidget for each top-level widget you create to
#     ensure that they are properly closed after the test ends.
#     """
#     result = QtBot(request)
#     return result


# def test_pop_up_window():
#     """
#     Testing the pop up window view
#     """
#     model = main_model.MainModel()
#     controller = main_controller.MainController(model)
#     popup_window = Popup(controller)
#     popup_window.show()

#     qtbot.addWidget(popup_window)

#     # then you can use qtbot to test things


# def test_image_window():
#     """
#     Testing the main window view
#     """
#     model = main_model.MainModel()
#     controller = main_controller.MainController(model)
#     main_window = MainView(model, controller)
#     main_window.show()

#     qtbot.addWidget(main_window)

#     # then you can use qtbot to test things

#     # enter directory
#     # main_window.directory_input_text.clear()
#     # qtbot.keyClicks(main_window.directory_input_text,
#     # 'E:/Documents/UNI/dicom_test_file')
#     # click the cell
#     # qtbot.mouseClick(main_window.files_table)
