"""Established MainView class"""
import os

from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QTableWidgetItem,
    QTableWidget,
    QAbstractItemView,
    QHeaderView,
    QLineEdit,
)
# pylint: disable = E1101
from Custom_Logging.logger import CustLogger

#call logging
logging_display = CustLogger(name=__name__)

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
            self._main_controller.browse_for_dicom_file_directory)

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
        # listening for change in selected directory
        self._model.selected_dicom_directory_changed.connect(
            self.on_selected_dicom_directory_changed
        )

        # checks for default directory preference in config db
        self._main_controller.check_preference()

    def on_selected_dicom_directory_changed(self, path):
        """
        Displays all DICOM image files in a table with name and size
        """

        self.directory_input_text.setText(path)

        self.files_table.setRowCount(0)
        files = self._main_controller.get_dicom_image_files_in_selected_path(
            path)

        for absolute_path in files:
            current_image_file_size = os.path.getsize(absolute_path)

            file_name = absolute_path.split("/")[-1]

            file_name_item = QTableWidgetItem(file_name)

            kb_files_size = int((current_image_file_size + 1023) / 1024)
            size_item = QTableWidgetItem(
                f"{kb_files_size} KB")

            row = self.files_table.rowCount()
            self.files_table.insertRow(row)
            self.files_table.setItem(row, 0, file_name_item)
            self.files_table.setItem(row, 1, size_item)

        files_found_str = f"{len(files)} file(s) \
        found (Click on a file to open it)"
        self.files_found_label.setText(files_found_str)

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
