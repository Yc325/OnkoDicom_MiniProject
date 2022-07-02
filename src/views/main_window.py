"""Established MainView class"""
import os
import tkinter as tk
from tkinter import ttk
from views.image_window import ImageWindow
from os.path import dirname

# pylint: disable = E1101
from custom_logging.logger import CustLogger

# call logging
logging_display = CustLogger(name=__name__)


class MainView():
    """
    Handles main window (UI) displayed to user
    """

    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller

        # set window title + window size
        self.root_window = tk.Tk()
        self.root_window.geometry("600x600")
        self.root_window.title('View DICOM files')

        # configure the grid
        # self.root_window.columnconfigure(0, weight=1)
        # self.root_window.columnconfigure(1, weight=5)
        # self.root_window.columnconfigure(2, weight=1)

        # directory label: "In directory"
        directory_label = ttk.Label(self.root_window, text="In directory:")
        directory_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        # directory text input
        directory_input = ttk.Entry(self.root_window, width=45)
        directory_input.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        # directory search button
        dir_search_button = ttk.Button(self.root_window, text="Change...", command=self._main_controller.browse_for_dicom_file_directory)
        dir_search_button.grid(column=2, row=0, sticky=tk.E, padx=5, pady=5)

        btn = ttk.Button(self.root_window,
             text ="Click to open image window")

        parent_directory = dirname(__file__).split("\\src")[0]
        image_path = f"{parent_directory}\\dicom_file\\CT_183_Hashed.dcm"
        self._main_controller.change_selected_image_file_path(image_path)

        btn.bind("<Button>",
                lambda e: self._main_controller.change_selected_image_file_path(image_path)
                )

        btn.grid(column=1, row=1)

        # Create GRID LAYOUT
        # main_layout = QGridLayout()
        # main_layout.addWidget(directory_label, 2, 0)
        # main_layout.addWidget(self.directory_input_text, 2, 1)
        # main_layout.addWidget(self.browse_files_button, 2, 2)
        # main_layout.addWidget(self.files_table, 3, 0, 1, 3)
        # main_layout.addWidget(self.files_found_label, 4, 0)
        # main_layout.addLayout(buttons_layout, 5, 0, 1, 3)

        # connect widgets to controller
        # self.directory_input_text.textChanged.connect(
        #     self._main_controller.change_selected_dicom_directory
        # )
        # rather than calling the main_controller directly
        # an intermittent function is required to get/present the data
        # self.files_table.cellClicked.connect(self.select_image_file)

        # listen for model event signals
        # listening for change in selected directory
        # self._model.selected_dicom_directory_changed.connect(
        #     self.on_selected_dicom_directory_changed
        # )

        # checks for default directory preference in config db
        self._main_controller.check_preference()

    def show(self):
        self.root_window.mainloop()

    def on_selected_dicom_directory_changed(self, path):
        """
        Displays all DICOM image files in a table with name and size
        """

        self.directory_input_text.setText(path)

        self.files_table.setRowCount(0)
        files = self._main_controller.get_dicom_image_files_in_selected_path()

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
