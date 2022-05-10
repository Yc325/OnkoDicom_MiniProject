import sys
from PyQt6.QtWidgets import QApplication
from models.MainModel import MainModel
from controllers.MainController import MainController
from views.MainWindow import MainView


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = MainModel()
        self.main_controller = MainController(self.model)
        self.main_view = MainView(self.model, self.main_controller)
        self.main_view.show()

if __name__ == '__main__':
    app = App(sys.argv)
    app.exec()
    sys.exit(app.exec_())