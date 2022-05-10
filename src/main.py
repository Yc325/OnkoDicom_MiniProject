"""
The main function which starts the entire application
"""

import sys
from PyQt6.QtWidgets import QApplication
from models.main_model import MainModel
from controllers.main_controller import MainController
from views.main_window import MainView

class App(QApplication):
    """
    Main Application code that instantiates model, view, controller
    """
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.model = MainModel()
        self.main_controller = MainController(self.model)
        self.main_view = MainView(self.model, self.main_controller)
        self.main_view.show()

if __name__ == '__main__':
    app = App(sys.argv)
    app.exec()
    sys.exit(app.exec_())
