"""
Declares class for ImageWindow
"""
# pylint: disable=E1101
# pylint: disable=C0413
import sys
import numpy as np
from PySide6.QtWidgets import (QLabel,
                               QPushButton,
                               QWidget,
                               QGridLayout,
                               )
from PySide6 import QtCore, QtGui
# WARNING: this is required because of ImageQt backend issues
# need to clean up our imports/dependencies as it is very fragile
sys.modules['PyQt6.QtGui'] = QtGui
from PIL import Image, ImageQt  # noqa: E402


class ImageWindow(QWidget):
    """
    The window that displays the dicom image,
    arrows to navigate through multiple images,
    and name and number of image file.
    """

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
        dicom_file_parser = self._main_controller.get_dicom_image_parser()
        dataset = dicom_file_parser.get_dataset()

        # Try turn pixel data into image
        # from
        # https://github.com/pydicom/contrib-pydicom/blob/master/viewers/pydicom_PIL.py
        win_width = dataset['WindowWidth']
        win_center = dataset['WindowCenter']

        window = int(
            win_width.value[0] if win_width.VM > 1 else win_width.value)
        level = int(
            win_center.value[0] if win_center.VM > 1 else win_center.value)
        # Takes Data Value if IMG (pixels)
        data = dataset.pixel_array
        # using numpy library
        np_image = np.piecewise(data,
                                [data <= (level - 0.5 - (window - 1) / 2),
                                 data > (level - 0.5 + (window - 1) / 2)],
                                [0,
                                 255,
                                 lambda data: ((data - (level - 0.5)) /
                                               (window - 1) + 0.5)*(255 - 0)])

        # Using PIL library
        pillow_image = Image.fromarray(np_image).convert('L')

        qt_image = ImageQt.ImageQt(pillow_image)

        self.image_window.setPixmap(QtGui.QPixmap.fromImage(qt_image))

        self.image_title_label.setText(
            f'Body Part: {dicom_file_parser.get_body_part_title()}')
        self.image_number.setText(
            f'IMG # {dicom_file_parser.get_image_number()}')
