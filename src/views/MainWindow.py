from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import pyqtSlot, QDir, QFile, QFileInfo
from PyQt6 import QtCore
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
                               QLineEdit,
                               )
import os

class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller

        # directory search bar
        self.browse_files_button = QPushButton("&Browse...")
        self.browse_files_button.clicked.connect(self.browse_for_dicom_file_directory)

        directory_input_text = QLineEdit()
        directory_input_text.setText(QDir.currentPath())
        # comboBox.setSizePolicy(QSizePolicy.Expanding,
        #                        QSizePolicy.Preferred)

        self.directory_input_text = directory_input_text

        directoryLabel = QLabel("In directory:")
        self.filesFoundLabel = QLabel()

        self.filesTable = QTableWidget(0, 2)
        self.filesTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.filesTable.setHorizontalHeaderLabels(("File Name", "Size",None))
        self.filesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        # self.filesTable.verticalHeader().hide()
        # self.filesTable.hideColumn(2) #hide column
        self.filesTable.setShowGrid(False)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch()

        #Create GRID LAYOUT
        mainLayout = QGridLayout()
        mainLayout.addWidget(directoryLabel, 2, 0)
        mainLayout.addWidget(self.directory_input_text, 2, 1)
        mainLayout.addWidget(self.browse_files_button, 2, 2)
        mainLayout.addWidget(self.filesTable, 3, 0, 1, 3)
        mainLayout.addWidget(self.filesFoundLabel, 4, 0)
        mainLayout.addLayout(buttonsLayout, 5, 0, 1, 3)

        container = QWidget()
        container.setLayout(mainLayout)
        self.setWindowTitle("Explore DICOM Files")
        self.resize(600, 600)
        self.setCentralWidget(container)

        # connect widgets to controller
        self.directory_input_text.textChanged.connect(self._main_controller.change_selected_dicom_directory)
        
        # rather than calling the main_controller directly
        # an intermittent function is required to get/present the data
        self.filesTable.cellClicked.connect(self.selectImageFile)

        # listen for model event signals
        # self._model.amount_changed.connect(self.on_amount_changed)
        # listening for change in selected directory
        self._model.selected_dicom_directory_changed.connect(self.on_selected_dicom_directory_changed)

    # @pyqtSlot(str)
    def on_selected_dicom_directory_changed(self, path):
        try:
            self.filesTable.setRowCount(0)

            self.currentDir = QDir(path)
            fileName = "*.dcm"
            # files = self.currentDir.entryList([fileName],
            #                                     QDir.Files | QDir.NoSymLinks)

            files = os.listdir(path)

            for file_name in files:
                file = QFile(self.currentDir.absoluteFilePath(file_name))
                size = QFileInfo(file).size()

                fileNameItem = QTableWidgetItem(file_name)

                fileNameNumber = (''.join(filter(str.isdigit,file_name))) #get number from the name of the file

                # For sorting items and adding them to hidden column
                # if 'RT' not in file_name:
                #     Item_number = QTableWidgetItem()
                #     Item_number.setData(QtCore.Qt.EditRole, int(fileNameNumber))
                #     Item_number.setFlags(Item_number.flags() ^ Qt.ItemIsEditable)
                # else:
                #     print(fileNameNumber)
                #     Item_number = QTableWidgetItem('RT')
                #     Item_number.setFlags(Item_number.flags() ^ Qt.ItemIsEditable)


                # fileNameItem.setFlags(fileNameItem.flags() ^ Qt.ItemIsEditable)
                sizeItem = QTableWidgetItem("%d KB" % (int((size + 1023) / 1024))) #Caluclate size
                # sizeItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                # sizeItem.setFlags(sizeItem.flags() ^ QtCore.Qt.ItemIsEditable)


                row = self.filesTable.rowCount()
                self.filesTable.insertRow(row)
                self.filesTable.setItem(row, 0, fileNameItem)
                self.filesTable.setItem(row, 1, sizeItem)
                # self.filesTable.setItem(row, 2, Item_number) #insert row of file number

            # self.filesFoundLabel.setText("%d file(s) found (Double click on a file to open it)" % len(files))
            # self.filesTable.sortItems(2, order=QtCore.Qt.AscendingOrder)
        except Exception as e:
            print(e)

    def selectImageFile(self, row, column):
        print(row, column)
        # gets path from selected cell choice
        item = self.filesTable.item(row, 0)
        path = self.directory_input_text.text() + "/" + item.text()
        
        # sends to controller
        self._main_controller.change_selected_image_file_path(path)

    def browse_for_dicom_file_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Find Files",
                                                               QDir.currentPath())

        # allows update of text box when directory changes?
        if directory:
            if self.directory_input_text.text() != directory:
                self.directory_input_text.setText(directory)

# class MainWindow(QMainWindow):
#     def __init__(self, model, main_controller):
#         super().__init__()

#         self.w = True  # No external window yet.
#         #set window Title
#         self.setWindowTitle('OnkoDicom')
#         #Create 2 Buttons
#         button_suc = QPushButton("Open Dicom File")
#         button_close = QPushButton("Force Quit",self)
#         #Assign Buttons
#         # button_suc.clicked.connect(self.Window_to_browse_DICOM_files)
#         # button_close.clicked.connect(QApplication.instance().quit)

#         label = QLabel("InkoDICOM")
#         # label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # set aligment

#         #Create LOGO of DICOM
#         pixmap = QPixmap('./img/logo.png')
#         pixmap = pixmap.scaled(200,200, Qt.KeepAspectRatio)
#         label.setPixmap(pixmap)  # add img

#         #Create Grid layout to properly locate the buttons and other widgets
#         layout = QGridLayout()
#         layout.addWidget(label, 0, 0, 3, 5, Qt.AlignCenter ) #Add label
#         layout.addWidget(button_suc, 3, 0) #Add button
#         layout.addWidget(button_close, 3, 4) #Add button

#         #Create Container and add layout to it.
#         container = QWidget()
#         container.setLayout(layout)

#         #Run it
#         self.setCentralWidget(container)