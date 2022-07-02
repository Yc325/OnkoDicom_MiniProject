"""
The main function which starts the entire application
"""

import sys
from PyQt6.QtWidgets import QApplication
from models.main_model import MainModel
from controllers.main_controller import MainController
from views.main_window import MainView
from custom_logging.logger import CustLogger
logging_display = CustLogger(name=__name__)


class App(QApplication):
    """
    Main Application code that instantiates model, view, controller
    """
    # display logging info
    logging_display.logger.info('Class created')

    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.model = MainModel()
        self.main_controller = MainController(self.model)
        self.main_view = MainView(self.model, self.main_controller)
        self.main_view.show()


if __name__ == '__main__':
    # Add info to display anything what it is called
    # logging_display.logger.info("info")
    # like critical error
    # logging_display.logger.critical("critical")
    # debug
    # logging_display.logger.debug("debug")
    # error
    # logging_display.logger.error("error")
    # exception
    # logging_display.logger.exception("exception")
    # warning
    # logging_display.logger.warning("Warning")
    app = App(sys.argv)
