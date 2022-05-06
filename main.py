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
from PySide6.QtGui import QPixmap,QCloseEvent
import sys
import pydicom
import os
import matplotlib.pyplot as plt
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

        pixmap = QPixmap('img/logo.png')
        pixmap = pixmap.scaled(200,200, Qt.KeepAspectRatio)

        label.setPixmap(pixmap)  # add img

        layout = QGridLayout()
        layout.addWidget(label, 0, 0, 3, 5, Qt.AlignCenter )
        layout.addWidget(button_suc, 3, 0)
        layout.addWidget(button_close, 3, 4)
        layout.addWidget(button_close, 3, 4)
        layout.addWidget(self.image_label,5,0,3,5,Qt.AlignCenter)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
    #Button to close window
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
    def browse(self):
        qfd = QFileDialog()
        path = os.getcwd()
        filter = "dcm(*.dcm)"
        f = QFileDialog.getOpenFileName(qfd,'Open dcm File', path, filter)
        print(f[0])
        self.openFileOfItem(f[0])

    #Display Dicom File
    def displayDicomInformation(self, msg):
        infoDialog = QDialog()
        layout = QGridLayout(infoDialog)
        layout.addWidget(QLabel(msg))
        infoDialog.setLayout(layout)
        infoDialog.setWindowTitle('Dicom tag information')
        infoDialog.show()
        infoDialog.exec()
    #Display IMG
    def displayDicomImgageWindow(self,im):
        Windiw_Image= QLabel()
        Windiw_Image.setPixmap(QPixmap.fromImage(im))
        Windiw_Image.show()
        Windiw_Image.exec()


    #Open File
    def openFileOfItem(self, path):
        dataset = pydicom.dcmread(path)

        all_tags = ''
        for elem in dataset:
            tag = str(elem) + '\n'
            all_tags += tag

        self.displayDicomInformation(all_tags)
        self.displayDicomImage(dataset)
    #Display DICOM Img
    def displayDicomImage(self, ds):
        # Try turn pixel data into image
        # from https://github.com/pydicom/contrib-pydicom/blob/master/viewers/pydicom_PIL.py
        ew = ds['WindowWidth']
        ec = ds['WindowCenter']
        ww = int(ew.value[0] if ew.VM > 1 else ew.value)
        wc = int(ec.value[0] if ec.VM > 1 else ec.value)
        data = ds.pixel_array
        print(data)
        window = ww
        level = wc
        image = np.piecewise(data,
                             [data <= (level - 0.5 - (window - 1) / 2),
                              data > (level - 0.5 + (window - 1) / 2)],
                             [0, 255, lambda data: ((data - (level - 0.5)) /
                                                    (window - 1) + 0.5) * (255 - 0)])
        im = Image.fromarray(image).convert('L')

        im = ImageQt(im)
        self.image_label.setPixmap(QPixmap.fromImage(im))
        self.displayDicomImgageWindow(im)




app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()