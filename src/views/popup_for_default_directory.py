"""Popup window for selecting directory and setting in hidden DB config"""
from PyQt6.QtCore import QDir
from PySide6.QtWidgets import (
    QFileDialog,
    QDialog,
    QPushButton,
    QLineEdit,
    QLabel,
    QHBoxLayout)
# pylint: disable = E1101


class Popup(QDialog):
    """
    Creates Popup Window For User To Find DICOM Files
    """

    def __init__(self, main_controller):
        super().__init__()

        self._main_controller = main_controller
        self.resize(500, 250)

        self.directory_label = QLabel("Directory:", self)
        self.directory_input_text = QLineEdit(self)
        self.browse_files = QPushButton("&Browse...")

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.directory_label)
        self.layout.addWidget(self.directory_input_text)
        self.layout.addWidget(self.browse_files)

        self.browse_files.clicked.connect(
            self.browse_directory)

    def browse_directory(self):
        """
        Opens window to allow user to browse directories on their computer
        and select a dicom file
        """
        # User can choose directory
        directory = QFileDialog.getExistingDirectory(self, "Find Files",
                                                     QDir.currentPath())
        # updates database with new directory
        self._main_controller.get_config().update_default_dir(directory)
        
        # asks the main controller to recheck db for directoy
        self._main_controller.check_preference()
        self.close()
