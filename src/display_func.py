#import Libraries
from PySide6.QtWidgets import (QApplication,
                                QLabel,
                                QMainWindow,
                                QPushButton,
                                QWidget,
                                QGridLayout,
                                QMessageBox,
                                QFileDialog,
                                QDialog,
                                QGridLayout,
                                QHBoxLayout,
                               QTableWidgetItem,
                               QComboBox,
                               QSizePolicy,
                               QTableWidget,
                               QAbstractItemView,
                               QHeaderView,
                               )

from PySide6.QtCore import Qt,QDir,QFile,QFileInfo
from PySide6.QtGui import QPixmap, QCloseEvent,QAction, QIcon
import sys
import pydicom
import os

from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np
import re
# Display Dicom File
"""
Function that creates new window to display Dicom information from choosen file
The input of the function takes msg of the DICOM file and create it in new Window
Basically it just GUI functions that creates new window with msg
"""


# def displayDicomInformation(self, msg):
#     infoDialog = QDialog()
#     layout = QGridLayout(infoDialog)
#     layout.addWidget(QLabel(msg))
#     infoDialog.setLayout(layout)
#     infoDialog.setWindowTitle('Dicom tag information')
#     infoDialog.show()
#     infoDialog.exec()


# Display img in a new window
"""
Function that creates new window to display Dicom IMG from chosen file
The input of the function takes IMG of the DICOM file and create it in new Window
Basically it just GUI functions that creates new window with IMG
"""


def displayDicomImgageWindow(self,
                             im,
                             text,
                             img_n,
                             all_tags):


    Window_Image = QLabel()
    Window_Image.setPixmap(QPixmap.fromImage(im))

    Image_partBody = QLabel()
    Image_partBody.setText(f'Body Part: {text}')

    Img_number = QLabel()
    Img_number.setText(f'IMG # {img_n}')

    button_action_left = QPushButton(None)
    button_action_left.setIcon(QIcon("./icons/arrow-180-medium.png"))

    button_action_right = QPushButton(None)
    button_action_right.setIcon(QIcon("./icons/arrow-000-medium.png"))

    #FUNCTION FOR BUTTONS
    #_______
    #Left
    #Button goes to IMG-1
    #Right
    #button goes to IMG+1
    #_______
    layout = QGridLayout()
    layout.addWidget(Img_number, 1,0,1,5,Qt.AlignCenter)
    layout.addWidget(Image_partBody,3,0,1,5,Qt.AlignCenter)
    layout.addWidget(button_action_left,2,0)
    layout.addWidget(button_action_right,2,4)
    layout.addWidget(Window_Image,4,0,4,5,Qt.AlignCenter)


    container = QWidget()
    container.setLayout(layout)
    container.setWindowTitle(f'Dicom Image')

    container.show()
    container.exec()


"""
Function that take input of the chosen path and create proper msg from the DICOM file
Then it calls function "displayDicomInformation" with prepared msg
That function contains function "displayDicomImage" it takes DICOM file as input
and prepare IMG
"""

# Display DICOM Img
""""
Function that prepare DICOM FILE to be Displayed
"""


def displayDicomImage(self, ds,all_tags):
    # Try turn pixel data into image
    # from https://github.com/pydicom/contrib-pydicom/blob/master/viewers/pydicom_PIL.py
    ew = ds['WindowWidth']  # it takes value from DICOM FILE that has key 'Window Width'
    ec = ds['WindowCenter']  # it takes value from DICOM FILE that has key 'Window Center'
    text = ds['BodyPartExamined'] #it take value from Dicom file that has ket 'Body Part Examined'
    IMG_number = ds['InstanceNumber'] #it take value from Dicom file that has ket 'Instance Number'
    ww = int(ew.value[0] if ew.VM > 1 else ew.value)
    wc = int(ec.value[0] if ec.VM > 1 else ec.value)
    # Takes Data Value if IMG (pixels)
    data = ds.pixel_array
    print(data)
    window = ww
    level = wc
    # using numpy library
    image = np.piecewise(data,
                         [data <= (level - 0.5 - (window - 1) / 2),
                          data > (level - 0.5 + (window - 1) / 2)],
                         [0, 255, lambda data: ((data - (level - 0.5)) /
                                                (window - 1) + 0.5) * (255 - 0)])

    print(type(image), image)
    
    # Using PIL library
    im = Image.fromarray(image).convert('L')
    print(type(im), im)

    # Using PIL library
    im = ImageQt(im)
    print(type(im), im)
    displayDicomImgageWindow(self,im,text.value,IMG_number.value,all_tags) # call function displayDicomImgageWindow with provided img to display it in a new window
