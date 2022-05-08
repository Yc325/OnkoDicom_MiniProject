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
                                QGridLayout)

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QCloseEvent
import sys
import pydicom
import os

from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np



class MainWindow(QMainWindow):


    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.

        #set window Title
        self.setWindowTitle('OnkoDicom')
        #Create 2 Buttons
        button_suc = QPushButton("Open Dicom File")
        button_close = QPushButton("Force Quit",self)
        #Assign Buttons
        button_suc.clicked.connect(self.browse)
        button_close.clicked.connect(QApplication.instance().quit)

        label = QLabel("InkoDICOM")
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # set aligment

        #Make IMG for DICOM FILE
        self.image_label = QLabel()

        #Create LOGO of DICOM
        pixmap = QPixmap('img/logo.png')
        pixmap = pixmap.scaled(200,200, Qt.KeepAspectRatio)
        label.setPixmap(pixmap)  # add img

        #Create Grid layout to properly locate the buttons and other widgets
        layout = QGridLayout()
        layout.addWidget(label, 0, 0, 3, 5, Qt.AlignCenter ) #Add label
        layout.addWidget(button_suc, 3, 0) #Add button
        layout.addWidget(button_close, 3, 4) #Add button
        layout.addWidget(self.image_label,5,0,3,5,Qt.AlignCenter)  #Add IMG of DICOM FILES

        #Create Container and add layout to it.
        container = QWidget()
        container.setLayout(layout)

        #Run it
        self.setCentralWidget(container)


    #Button to close window
    """
    This function alllows you to set notification to close window
    
    """
    def closeEvent(self, event: QCloseEvent):
        reply = QMessageBox.question(
            self,
            'Message',
            'Are you sure you want to quit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    #Window Dicom File
    """
    Function that allows you to  open Directory of your PC and choose DICOM File
    """
    def browse(self):
        qfd = QFileDialog() #File Dialog
        path = os.getcwd() #pick the current Directory of the File
        filter = "dcm(*.dcm)"   #set condition to choose only Dicom files
        f = QFileDialog.getOpenFileName(qfd,'Open dcm File', path, filter) #Premade functon to get the path of the chosen directory

        self.openFileOfItem(f[0]) #pick the chosen directory

    #Display Dicom File
    """
    Function that creates new window to display Dicom information from choosen file
    The input of the function takes msg of the DICOM file and create it in new Window
    Basically it just GUI functions that creates new window with msg
    """
    def displayDicomInformation(self, msg):
        infoDialog = QDialog()
        layout = QGridLayout(infoDialog)
        layout.addWidget(QLabel(msg))
        infoDialog.setLayout(layout)
        infoDialog.setWindowTitle('Dicom tag information')
        infoDialog.show()
        infoDialog.exec()

    #Display img in a new window
    """
    Function that creates new window to display Dicom IMG from chosen file
    The input of the function takes IMG of the DICOM file and create it in new Window
    Basically it just GUI functions that creates new window with IMG
    """
    def displayDicomImgageWindow(self,im):
        Windiw_Image= QLabel()
        Windiw_Image.setPixmap(QPixmap.fromImage(im))
        Windiw_Image.show()
        Windiw_Image.exec()

    """
    Function that take input of the chosen path and create proper msg from the DICOM file
    Then it calls function "displayDicomInformation" with prepared msg
    That function contains function "displayDicomImage" it takes DICOM file as input
    and prepare IMG
    """
    #Open File
    def openFileOfItem(self, path):
        dataset = pydicom.dcmread(path)

        all_tags = ''
        for elem in dataset:
            tag = str(elem) + '\n'
            all_tags += tag

        self.displayDicomInformation(all_tags) #Show the msg in a new window
        self.displayDicomImage(dataset) #Takes DICOM File

    #Display DICOM Img
    """"
    Function that prepare DICOM FILE to be Displayed
    """
    def displayDicomImage(self, ds):
        # Try turn pixel data into image
        # from https://github.com/pydicom/contrib-pydicom/blob/master/viewers/pydicom_PIL.py
        ew = ds['WindowWidth']  #it takes value from DICOM FILE that has key 'WindowWidth'
        ec = ds['WindowCenter'] #it takes value from DICOM FILE that has key 'WindowCenter'
        ww = int(ew.value[0] if ew.VM > 1 else ew.value)
        wc = int(ec.value[0] if ec.VM > 1 else ec.value)
        #Takes Data Value if IMG (pixels)
        data = ds.pixel_array
        window = ww
        level = wc
        #using numpy library
        image = np.piecewise(data,
                             [data <= (level - 0.5 - (window - 1) / 2),
                              data > (level - 0.5 + (window - 1) / 2)],
                             [0, 255, lambda data: ((data - (level - 0.5)) /
                                                    (window - 1) + 0.5) * (255 - 0)])
        #Using PIL library
        im = Image.fromarray(image).convert('L')
        # Using PIL library
        im = ImageQt(im)

        self.image_label.setPixmap(QPixmap.fromImage(im)) #Assign image_label DICOM img
        self.displayDicomImgageWindow(im) #call function displayDicomImgageWindow with provided img to display it in a new window




app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()