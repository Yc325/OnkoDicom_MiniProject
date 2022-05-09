import PySide6
from PySide6 import QtCore, QtGui
import sys
# this is required because of ImageQt backend issues
# TODO: need to clean up our imports/dependencies as it is very fragile
sys.modules['PyQt6.QtGui'] = QtGui

#import Libraries
from PySide6.QtWidgets import ( QApplication,
                                QLabel,
                                QPushButton,
                                QWidget,
                                QGridLayout,
                                QGridLayout,
                                QTableWidget,
                               )

import PIL
from PIL import Image, ImageQt
import numpy as np
from PySide6.QtGui import QPixmap

class ImageWindow(QWidget):
    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller

        image_window = QLabel()

        dicom_file_parser = self._main_controller.getDicomParser()
        dataset = dicom_file_parser.getDataSet()

        # Try turn pixel data into image
        # from https://github.com/pydicom/contrib-pydicom/blob/master/viewers/pydicom_PIL.py
        ew = dataset['WindowWidth']  # it takes value from DICOM FILE that has key 'Window Width'
        ec = dataset['WindowCenter']  # it takes value from DICOM FILE that has key 'Window Center'
        
        ww = int(ew.value[0] if ew.VM > 1 else ew.value)
        wc = int(ec.value[0] if ec.VM > 1 else ec.value)
        
        # Takes Data Value if IMG (pixels)
        data = dataset.pixel_array
        window = ww
        level = wc
        # using numpy library
        np_image = np.piecewise(data,
                            [data <= (level - 0.5 - (window - 1) / 2),
                            data > (level - 0.5 + (window - 1) / 2)],
                            [0, 255, lambda data: ((data - (level - 0.5)) /
                                                    (window - 1) + 0.5) * (255 - 0)])

        # print(type(np_image), np_image)

        # Using PIL library
        im = Image.fromarray(np_image).convert('L')

        # print(type(im), im)

        pillow_image = ImageQt.ImageQt(im)

        # print(type(pillow_image), pillow_image)

        image_window.setPixmap(QtGui.QPixmap.fromImage(pillow_image))

        image_title_label = QLabel()
        image_title_label.setText(f'Body Part: {dicom_file_parser.getBodyPartTitle()}')

        image_number = QLabel()
        image_number.setText(f'IMG # {dicom_file_parser.getImageNumber()}')

        button_action_left = QPushButton(None)
        button_action_left.setIcon(QtGui.QIcon("./icons/arrow-180-medium.png"))
        button_action_left.clicked.connect(self._main_controller.get_previous_image_file_path)

        button_action_right = QPushButton(None)
        button_action_right.setIcon(QtGui.QIcon("./icons/arrow-000-medium.png"))
        button_action_right.clicked.connect(self._main_controller.get_next_image_file_path)

        layout = QGridLayout()
        layout.addWidget(image_number, 1,0,1,5,QtCore.Qt.AlignCenter)
        layout.addWidget(image_title_label,3,0,1,5,QtCore.Qt.AlignCenter)
        layout.addWidget(button_action_left,2,0)
        layout.addWidget(button_action_right,2,4)
        layout.addWidget(image_window,4,0,4,5,QtCore.Qt.AlignCenter)

        self.setLayout(layout)
        self.setWindowTitle(f'Dicom Image')