"""Tests the popup window"""

from models import main_model
from controllers import main_controller
from views.popup_for_default_directory import Popup


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
