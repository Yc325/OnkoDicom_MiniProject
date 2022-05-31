
"""Testing the main window"""
from models import main_model
from controllers import main_controller
from views.main_window import MainView


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
