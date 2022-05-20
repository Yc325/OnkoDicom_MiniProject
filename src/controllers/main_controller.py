"""
Established MainController class
"""
import os
import collections
from PySide6.QtCore import QObject
from models.dicom_file_parser_model import DicomFileModel
from models.configuration import Configuration
from views.image_window import ImageWindow
from views.popup_for_default_directory import Popup
from Custom_Logging.logger import CustLogger

# call logging
logging_display = CustLogger(name=__name__)


class MainController(QObject):
    """
    Main controller that handles application logic
    """
    logging_display.logger.info('Class created')

    def __init__(self, model):
        super().__init__()

        self._model = model
        self.dicom_image_window = None
        self.dicom_file_parser = None
        self._config = Configuration()

    def sort_list_of_files(self, path=None):
        """
        Returns a sorted list of DICOM
         image files in the
        current selected directory
        """
        # display logging info
        logging_display.logger.info('get_dicom_image_files_in_selected_path'
                                    ' function called')
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
            dicom_parser_instance = DicomFileModel(file)
            if dicom_parser_instance.get_type() == "CT Image":
                number = dicom_parser_instance.get_instance_number()
                dictionary[file] = number

        sorted_list_of_tuples = sorted(dictionary.items(), key=lambda x: x[1])
        sorted_dict = collections.OrderedDict(sorted_list_of_tuples)

        return list(sorted_dict.keys())

    def change_selected_dicom_directory(self, value):
        """
        Changes selected dicom directory in model
        """
        # display logging info
        logging_display.logger.info('change_selected_dicom_directory '
                                    'function called')
        # check if it is a valid path first
        if os.path.exists(value):
            self._model.selected_dicom_directory = value
            self._model.sorted_list_of_image_files = self.sort_list_of_files(value)  # noqa: E501
        else:
            logging_display.logger.error('Function '
                                         'change_selected_dicom_directory'
                                         ' did not find a path')

    def change_selected_image_file_path(self, value):
        """
        changes the selected image file path
        """
        # display logging info
        logging_display.logger.info('change_selected_image_file_path'
                                    ' function called')
        # WARNING: the dicom_file_parser must be set before the model
        # is changed. This is because the model change will trigger
        # a refresh in the ImageWindow's data which will reference the
        # dicom_file_parser.
        self.dicom_file_parser = DicomFileModel(value)

        # this will emit signal to the Image view to refresh it's data
        self._model.selected_image_file_path = value

        # create ImageWindow() instance using same model if it does
        # not already exist
        if not self.dicom_image_window:
            self.dicom_image_window = ImageWindow(self._model, self)
        self.dicom_image_window.show()

    def get_previous_image_file_path(self):
        """
        Sets the previous image path in the directory in the model
        """
        # display logging info
        logging_display.logger.info('get_previous_image_file_path'
                                    ' function called')

        current_image_file_path = self._model.selected_image_file_path

        files = self.get_dicom_image_files_in_selected_path()

        try:
            index = (files.index(current_image_file_path) - 1) % len(files)
            new_path = f"{files[index]}"
            self.change_selected_image_file_path(new_path)
        except ValueError:
            # log error: ie. file not in path
            logging_display.logger.exception('get_previous_image_file_path '
                                             '- File not in a path')
            # should handle this better too?
            return

    def get_next_image_file_path(self):
        """
        Sets the next image path in the directory in the model
        """
        # display logging info
        logging_display.logger.info('get_next_image_file_path function called')

        current_image_file_path = self._model.selected_image_file_path

        files = self.get_dicom_image_files_in_selected_path()

        try:
            index = (files.index(current_image_file_path) + 1) % len(files)
            new_path = f"{files[index]}"
            self.change_selected_image_file_path(new_path)

        except ValueError:
            # log error: ie. file not in path
            logging_display.logger.exception('get_next_image_file_path '
                                             '- '
                                             'File not in a path')
            # should handle this better too?
            return

    def get_dicom_image_parser(self):
        """
        Returns the dicom parser object on the controller
        """
        # display logging info
        logging_display.logger.info('get_dicom_image_parser function called')
        return self.dicom_file_parser

    def get_dicom_image_files_in_selected_path(self):
        """
        Getter for the current list of image files in the model
        """
        return self._model.sorted_list_of_image_files

    def check_preference(self):
        """
        Checks User Preferences from the db
        and either stores it in the state model or
        prompts the user to select one if none
        already exists
        """
        # display logging info
        logging_display.logger.info('check_preference function called')
        # checks if user has a default directory save in the db
        directory = self._config.get_default_dir()
        if directory is None:
            # no directory found, therefore opens popup
            self.browse_for_dicom_file_directory()
        else:
            # There is a directory so it sets it in the model
            # setting this in the model triggers the main window
            # to update the contents it is displaying
            self.change_selected_dicom_directory(directory[0])

    def browse_for_dicom_file_directory(self):
        """
        Opens PopUp Window
        """
        # display logging info
        logging_display.logger.info('browse_for_dicom_file_directory'
                                    ' function called')
        pop = Popup(self)
        pop.exec()

    def get_config(self):
        """
        Gets the config object
        """
        # display logging info
        logging_display.logger.info('get_config function called')
        return self._config
