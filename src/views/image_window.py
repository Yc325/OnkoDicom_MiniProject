"""
Declares class for ImageWindow
"""
# pylint: disable=E1101
from PySide6.QtWidgets import (QLabel,
                               QPushButton,
                               QWidget,
                               QGridLayout,
                               )
from PySide6 import QtCore, QtGui
from src.Custom_Logging.logger import custLogger

#call logging
logging_display = custLogger(name=__name__)

class ImageWindow(QWidget):
    """
    The window that displays the dicom image,
    arrows to navigate through multiple images,
    and name and number of image file.
    """
    # display logging info
    logging_display.logger.info('Class created')

    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller

        self.image_window = QLabel()
        self.image_title_label = QLabel()
        self.image_number = QLabel()

        self.show_data()

        self.button_action_left = QPushButton(None)
        self.button_action_left.setIcon(
            QtGui.QIcon("./src/icons/arrow-180-medium.png"))
        self.button_action_left.clicked.connect(
            self._main_controller.get_previous_image_file_path)

        self.button_action_right = QPushButton(None)
        self.button_action_right.setIcon(
            QtGui.QIcon("./src/icons/arrow-000-medium.png"))
        self.button_action_right.clicked.connect(
            self._main_controller.get_next_image_file_path)

        layout = QGridLayout()
        layout.addWidget(self.image_number, 1, 0, 1, 5, QtCore.Qt.AlignCenter)
        layout.addWidget(self.image_title_label, 3, 0,
                         1, 5, QtCore.Qt.AlignCenter)
        layout.addWidget(self.button_action_left, 2, 0)
        layout.addWidget(self.button_action_right, 2, 4)
        layout.addWidget(self.image_window, 4, 0, 4, 5, QtCore.Qt.AlignCenter)

        self.setLayout(layout)
        self.setWindowTitle("Dicom Image")

        # actually subscribes the window to the model data as well
        self._model.selected_image_file_path_changed.connect(self.show_data)

    def show_data(self):
        """
        Refreshes all the data on the image window with reference to the
        DicomFileParserModel stored on the MainController
        """
        # display logging info
        logging_display.logger.info('show_data function called')

        dicom_file_parser = self._main_controller.get_dicom_image_parser()

        self.image_window.setPixmap(
            QtGui.QPixmap.fromImage(dicom_file_parser.get_qtimage())
            )

        self.image_title_label.setText(
            f'Body Part: {dicom_file_parser.get_body_part_title()}')
        self.image_number.setText(
            f'IMG # {dicom_file_parser.get_instance_number()}')
