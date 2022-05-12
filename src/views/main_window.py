"""Established MainView class"""
import os

from PIL.ImageEnhance import Color
from PyQt6.QtCore import QDir, QSize
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QTableWidgetItem,
    QTableWidget,
    QAbstractItemView,
    QHeaderView,
    QLineEdit, QMessageBox, QDialog,
)
# pylint: disable=E1101
import sys
from src.models.configuration import Configuration

config = Configuration()

class MainView(QMainWindow):
    """
    Handles main window (UI) displayed to user
    """

    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller

        # directory search button
        self.browse_files_button = QPushButton("&Change...")
        self.browse_files_button.clicked.connect(
            self.browse_for_dicom_file_directory)

        directory_input_text = QLineEdit()
        # directory_input_text.setText(QDir.currentPath())
        # comboBox.setSizePolicy(QSizePolicy.Expanding,
        #                        QSizePolicy.Preferred)

        self.directory_input_text = directory_input_text

        directory_label = QLabel("In directory:")
        self.files_found_label = QLabel()

        self.files_table = QTableWidget(0, 2)
        self.files_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.files_table.setHorizontalHeaderLabels(("File Name", "Size", None))
        self.files_table.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )
        # self.files_table.verticalHeader().hide()
        # self.files_table.hideColumn(2) #hide column
        self.files_table.setShowGrid(False)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        # Create GRID LAYOUT
        main_layout = QGridLayout()
        main_layout.addWidget(directory_label, 2, 0)
        main_layout.addWidget(self.directory_input_text, 2, 1)
        main_layout.addWidget(self.browse_files_button, 2, 2)
        main_layout.addWidget(self.files_table, 3, 0, 1, 3)
        main_layout.addWidget(self.files_found_label, 4, 0)
        main_layout.addLayout(buttons_layout, 5, 0, 1, 3)

        container = QWidget()
        container.setLayout(main_layout)
        self.setWindowTitle("Explore DICOM Files")
        self.resize(600, 600)
        self.setCentralWidget(container)

        # connect widgets to controller
        self.directory_input_text.textChanged.connect(
            self._main_controller.change_selected_dicom_directory
        )
        # rather than calling the main_controller directly
        # an intermittent function is required to get/present the data
        self.files_table.cellClicked.connect(self.select_image_file)

        # listen for model event signals
        # self._model.amount_changed.connect(self.on_amount_changed)
        # listening for change in selected directory
        self._model.selected_dicom_directory_changed.connect(
            self.on_selected_dicom_directory_changed
        )

        # checks for default directory
        self.check_preference()


    def check_preference(self):
        # checks if user has a default directory save in the db
        dir = config.get_default_dir()
        if dir is None:
            # no directory found, therefore opens popup
            self.browse_for_dicom_file_directory()
        else:
            # There is a directory so it displays files
            self.directory_input_text.setText(dir[0])
            self.on_selected_dicom_directory_changed(dir[0])


    def on_selected_dicom_directory_changed(self, path):
        """
        Displays all DICOM image files in a table with name and size
        """

        self.files_table.setRowCount(0)
        files = self._main_controller.get_dicom_image_files_in_selected_path(
            path)

        for absolute_path in files:
            current_image_file_size = os.stat(absolute_path).st_size

            file_name = absolute_path.split("/")[-1]

            file_name_item = QTableWidgetItem(file_name)

            # fileNameItem.setFlags(fileNameItem.flags() ^ Qt.ItemIsEditable)
            size_item = QTableWidgetItem(
                f"{(int((current_image_file_size + 1023) / 1024))} KB")
            # sizeItem.setTextAlignment(QtCore.Qt.AlignVCenter
            # *| QtCore.Qt.AlignRight)
            # sizeItem.setFlags(sizeItem.flags() ^ QtCore.Qt.ItemIsEditable)

            row = self.files_table.rowCount()
            self.files_table.insertRow(row)
            self.files_table.setItem(row, 0, file_name_item)
            self.files_table.setItem(row, 1, size_item)
            # self.files_table.setItem(row, 2, Item_number) #insert row of file
            # number

        # self.files_found_label.setText("%d file(s) found
        # (Double click on a file to open it)" % len(files))

    def select_image_file(self, row, column):
        """
        Sets image file in model from the selected cell
        """
        print(row, column)
        # gets path from selected cell choice
        item = self.files_table.item(row, 0)
        print(item.text())
        path = self.directory_input_text.text() + "/" + item.text()
        # sends to controller
        self._main_controller.change_selected_image_file_path(path)

    def browse_for_dicom_file_directory(self):
        """
        Opens PopUp Window
        """
        pop = Popup(self)
        pop.show()


class Popup(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.resize(500, 250)

        self.directory_label = QLabel("Directory:", self)
        self.directory_input_text = QLineEdit(self)
        self.browse_files = QPushButton("&Browse...")

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.directory_label)
        self.layout.addWidget(self.directory_input_text)
        self.layout.addWidget(self.browse_files)

        self.browse_files.clicked.connect(
            self.browse_directory)

    def browse_directory(self):
        """
        Opens window to allow user to browse directories on their computer
        and select a dicom file
        """
        # User can choose directory
        directory = QFileDialog.getExistingDirectory(self, "Find Files",
                                                     QDir.currentPath())
        # updates database with new directory
        config.update_default_dir(directory)
        # updates parent window with new directory
        self.parent().check_preference()
        self.close()


