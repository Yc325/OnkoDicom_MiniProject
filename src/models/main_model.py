"""Declares MainModel for the application"""
from PyQt6.QtCore import QObject, pyqtSignal

class MainModel(QObject):
    """
    Main model that serves as a cnetral data store for
    the application to maintain state
    """
    selected_dicom_directory_changed = pyqtSignal(str)
    selected_image_file_path_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self._selected_dicom_directory = ""
        self._selected_image_file_path = ""

    @property
    def selected_image_file_path(self):
        """
        Getter for the selected image file path
        """
        return self._selected_image_file_path

    @selected_image_file_path.setter
    def selected_image_file_path(self, value):
        self._selected_image_file_path = value
        self.selected_image_file_path_changed.emit(value)

    @property
    def selected_dicom_directory(self):
        """
        Getter for the selected dicom directory
        """
        return self._selected_dicom_directory

    @selected_dicom_directory.setter
    def selected_dicom_directory(self, value):
        self._selected_dicom_directory = value
        self.selected_dicom_directory_changed.emit(value)
