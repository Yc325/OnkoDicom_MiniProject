from PyQt6.QtCore import QObject, pyqtSignal

class MainModel(QObject):
    selected_dicom_directory_changed = pyqtSignal(str)
    selected_image_file_path_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self._selected_dicom_directory = ""
        self._selected_image_file_path = ""

    @property
    def selected_image_file_path(self):
        return self._selected_image_file_path

    @selected_image_file_path.setter
    def selected_image_file_path(self, value):
        self._selected_image_file_path = value
        self.selected_image_file_path_changed.emit(value)

    @property
    def selected_dicom_directory(self):
        return self._selected_dicom_directory

    @selected_dicom_directory.setter
    def selected_dicom_directory(self, value):
        self._selected_dicom_directory = value
        self.selected_dicom_directory_changed.emit(value)