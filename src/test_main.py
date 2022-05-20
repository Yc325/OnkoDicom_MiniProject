"""
Instantiating some classes
"""
from os.path import dirname
from models import dicom_file_parser_model, main_model, configuration
from controllers import main_controller
from views.main_window import MainView
from views.popup_for_default_directory import Popup
# from PyQt6.QtCore import Qt


def test_configuration():
    """
    Testing the configuration object which sets up the DB
    for storing the configuration settings
    """
    # WARNING: this needs to be called before the other tests
    # which rely on a default directory existing in the db
    config = configuration.Configuration()
    parent_directory = dirname(__file__).split("\\src")[0]
    config.update_default_dir(f"{parent_directory}\\dicom_file")


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


def test_pop_up_window(qtbot):
    """
    Testing the pop up window view
    """
    model = main_model.MainModel()
    controller = main_controller.MainController(model)
    popup_window = Popup(controller)
    # popup_window.show()

    qtbot.addWidget(popup_window)

    assert popup_window.directory_label.text() == "Directory:"

    # had issue with antivirus
    # qtbot.mouseClick(popup_window.browse_files, Qt.MouseButton.LeftButton)

    # then you can use qtbot to test things


def test_main_window(qtbot):
    """
    Testing the main window view
    """
    model = main_model.MainModel()
    controller = main_controller.MainController(model)
    main_window = MainView(model, controller)
    # main_window.show()

    qtbot.addWidget(main_window)

    # then you can use qtbot to test things

    # enter directory
    main_window.directory_input_text.clear()
    qtbot.keyClicks(main_window.directory_input_text, 'dicom_file')

    # click the cell
    # qtbot.mouseClick(main_window.files_table.itemAt(0, 0))


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

    # try press left and right buttons here?
