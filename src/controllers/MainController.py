from PySide6.QtCore import Qt,QDir,QFile,QFileInfo,QObject
from PySide6.QtGui import QPixmap, QCloseEvent,QAction, QIcon
import sys
import pydicom
import os
import re

from views.ImageWindow import ImageWindow

class DicomFileParser:
    def __init__(self, path):
        dataset = pydicom.dcmread(path)

        all_tags = ''
        for elem in dataset:
            tag = str(elem) + '\n'
            all_tags += tag

        self.dataset = dataset
        self.all_tags = all_tags
        self.body_part_title = dataset['BodyPartExamined'].value #it take value from Dicom file that has ket 'Body Part Examined'
        self.image_number = dataset['InstanceNumber'].value #it take value from Dicom file that has ket 'Instance Number'

    def getImageNumber(self):
        return self.image_number

    def getBodyPartTitle(self):
        return self.body_part_title

    def getDataSet(self):
        return self.dataset

class MainController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model

    # @pyqtSlot(str)
    def change_selected_dicom_directory(self, value):
        print(f"controller: {value}")
        self._model.selected_dicom_directory = value

    # @pyqtSlot(str)
    def change_selected_image_file_path(self, value):
        self._model.selected_image_file_path = value

        # any extra data that needataset to be changed
        
        self.dicom_file_parser = DicomFileParser(value)

        # create ImageWindow() instance using same model
        self.dicom_image_window = ImageWindow(self._model, self)
        self.dicom_image_window.show()
    
    def get_previous_image_file_path(self):
        current_image_file_path = self._model.selected_image_file_path

        files = os.listdir(self._model.selected_dicom_directory)
        index = files.index(current_image_file_path.split("/")[-1])-1

        new_path = f"{self._model.selected_dicom_directory}/{files[index]}"
        self.change_selected_image_file_path(new_path)
        print("image path: "+new_path)
        self.dicom_file_parser = DicomFileParser(new_path)

        # create ImageWindow() instance using same model
        self.dicom_image_window = ImageWindow(self._model, self)
        self.dicom_image_window.show()
    
    def get_next_image_file_path(self):
        current_image_file_path = self._model.selected_image_file_path

        files = os.listdir(self._model.selected_dicom_directory)
        index = files.index(current_image_file_path.split("/")[-1])+1

        new_path = f"{self._model.selected_dicom_directory}/{files[index]}"
        self.change_selected_image_file_path(new_path)
        print("image path: "+new_path)
        self.dicom_file_parser = DicomFileParser(new_path)

        # create ImageWindow() instance using same model
        self.dicom_image_window = ImageWindow(self._model, self)
        self.dicom_image_window.show()

    def getDicomParser(self):
        return self.dicom_file_parser