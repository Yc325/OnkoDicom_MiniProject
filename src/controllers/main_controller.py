"""
Established MainController class
"""
import os
import collections
from PySide6.QtCore import QObject
import pydicom
from models.dicom_file_parser_model import DicomFileModel
from views.image_window import ImageWindow

class MainController(QObject):
    """
    Main controller that handles application logic
    """
    def __init__(self, model):
        super().__init__()

        self._model = model
        self.dicom_image_window = None
        self.dicom_file_parser = None

    def change_selected_dicom_directory(self, value):
        """
        Changes selected dicom directory in model
        """
        self._model.selected_dicom_directory = value

    def change_selected_image_file_path(self, value):
        """
        changes the selected image file path
        """
        # WARNING: the dicom_file_parser must be set before the model
        # is changed. This is because the model change will trigger
        # a refresh in the ImageWindow's data which will reference the
        # dicom_file_parser.
        self.dicom_file_parser = DicomFileModel(value)

        # this will emit signal to the Image view to refresh it's data
        self._model.selected_image_file_path = value

        # create ImageWindow() instance using same model
        if not self.dicom_image_window:
            self.dicom_image_window = ImageWindow(self._model, self)
        self.dicom_image_window.show()

    def get_previous_image_file_path(self):
        """
        Sets the previous image path in the directory in the model
        """
        current_image_file_path = self._model.selected_image_file_path

        files = self.get_dicom_image_files_in_selected_path()
        index = (files.index(current_image_file_path)-1)%len(files)

        new_path = f"{files[index]}"
        self.change_selected_image_file_path(new_path)

    def get_next_image_file_path(self):
        """
        Sets the next image path in the directory in the model
        """
        current_image_file_path = self._model.selected_image_file_path

        files = self.get_dicom_image_files_in_selected_path()
        index = (files.index(current_image_file_path)+1)%len(files)

        new_path = f"{files[index]}"
        self.change_selected_image_file_path(new_path)

    def get_dicom_image_parser(self):
        """
        Returns the dicom parser object on the controller
        """
        return self.dicom_file_parser

    def get_dicom_image_files_in_selected_path(self, path=None):
        """
        Returns a sorted list of DICOM image files in the
        current selected directory
        """
        files = []

        if path:
            current_dir = path
        else:
            current_dir = self._model.selected_dicom_directory
        files = os.listdir(current_dir)
        filtered_files = []

        # filter by .dcm file_type
        for file in files:
            if file.endswith(".dcm"):
                filtered_files.append(f"{current_dir}/{file}")

        # sort in number order?
        # Not sure if this a universal naming standard though so
        # could be a flaky way of sorting
        dictionary = {}
        for file in filtered_files:
            number = get_instance_number_of_file(file)
            dictionary[file] = number

        sorted_list_of_tuples = sorted(dictionary.items(), key=lambda x: x[1])
        sorted_dict = collections.OrderedDict(sorted_list_of_tuples)

        return list(sorted_dict.keys())

# move this function somewhere more relevent
def get_instance_number_of_file(file):
    """
    Retrieves the instance number of a given .dcm file
    """
    dataset = pydicom.dcmread(file)
    return int(dataset["InstanceNumber"].value)
