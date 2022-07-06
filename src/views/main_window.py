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
        self.directory_label = ttk.Label(self.root_window, text="In directory:")
        self.directory_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        # directory text input
        self.directory_input_text_value = tk.StringVar()
        self.directory_input_text = ttk.Entry(
            self.root_window, 
            width=45,
            textvariable=self.directory_input_text_value,
            validate="focusout",
            validatecommand=self._on_change_in_directory_text
            )
        self.directory_input_text.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        # directory search button
        self.dir_search_button = ttk.Button(self.root_window, text="Change...", command=self._main_controller.browse_for_dicom_file_directory)
        self.dir_search_button.grid(column=2, row=0, sticky=tk.E, padx=5, pady=5)

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
        self._model.selected_dicom_directory_changed.connect(
            self.on_selected_dicom_directory_changed
        )

        # checks for default directory preference in config db
        self._main_controller.check_preference()

    def _on_change_in_directory_text():
        self._main_controller.change_selected_dicom_directory(self.directory_input_text_value)

    def show(self):
        self.root_window.mainloop()

    def on_selected_dicom_directory_changed(self, path):
        """
        Displays all DICOM image files in a table with name and size
        """
        self.directory_input_text.delete(0, tk.END)
        self.directory_input_text.insert(0, path)

        # self.files_table.setRowCount(0)
        files = self._main_controller.get_dicom_image_files_in_selected_path()

        row_index=2

        for absolute_path in files:
            file_name = absolute_path.split("/")[-1]

            btn = ttk.Button(self.root_window,
            text =file_name)

            btn.bind("<Button>",
                    lambda e: self._main_controller.change_selected_image_file_path(absolute_path)
                    )

            btn.grid(column=1, row=row_index)
            row_index+=1

            # current_image_file_size = os.path.getsize(absolute_path)

            # file_name = absolute_path.split("/")[-1]

            # file_name_item = QTableWidgetItem(file_name)

            # kb_files_size = int((current_image_file_size + 1023) / 1024)
            # size_item = QTableWidgetItem(
            #     f"{kb_files_size} KB")

            # row = self.files_table.rowCount()
            # self.files_table.insertRow(row)
            # self.files_table.setItem(row, 0, file_name_item)
            # self.files_table.setItem(row, 1, size_item)

    def select_image_file(self, row, column):
        """
        Sets image file in model from the selected cell
        """
        # gets path from selected cell choice
        item = self.files_table.item(row, 0)
        path = self.directory_input_text.text() + "/" + item.text()
        
        # sends to controller
        self._main_controller.change_selected_image_file_path(path)
