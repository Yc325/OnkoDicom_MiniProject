"""
Declares class for ImageWindow
"""
from custom_logging.logger import CustLogger

from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk

# call logging
logging_display = CustLogger(name=__name__)


class ImageWindow(Toplevel):
    """
    The window that displays the dicom image,
    arrows to navigate through multiple images,
    and name and number of image file.
    """
    # display logging info
    logging_display.logger.info('Class created')

    def __init__(self, model, main_controller, master = None):
        super().__init__(master = master)
        self.title("Image Window")
        self.geometry("700x700")

        self._model = model
        self._main_controller = main_controller

        self.image_window = Canvas(self, width=700,height=700)
        # self.image_title_label = Label(self)
        # self.image_number = Label(self)

        self.image_window.pack()

        self.show_data()

        # self.slider = QSlider(self, QtCore.Qt.Horizontal)
        # self.slider.setOrientation(QtCore.Qt.Horizontal)
        # self.slider.sliderMoved.connect(
        #     lambda: self._main_controller.update_image_file_path(
        #         self.slider.value()
        #         )
        #     )

        # layout = QGridLayout()
        # layout.addWidget(self.image_number, 1, 0, 1, 5, QtCore.Qt.AlignCenter)
        # layout.addWidget(self.image_title_label, 3, 0,
        #                  1, 5, QtCore.Qt.AlignCenter)
        # layout.addWidget(self.slider, 2, 0)
        # layout.addWidget(self.image_window, 4, 0, 4, 5, QtCore.Qt.AlignCenter)

        # self.setLayout(layout)
        # self.setWindowTitle("Dicom Image")

        # # actually subscribes the window to the model data as well
        # self._model.selected_image_file_path_changed.connect(self.show_data)

    def show_data(self):
        """
        Refreshes all the data on the image window with reference to the
        DicomFileParserModel stored on the MainController
        """
        logging_display.logger.info('show_data function called')

        dicom_file_parser = self._main_controller.get_dicom_image_parser()
        self.pil_image = dicom_file_parser.get_pil_image()
        self.image = ImageTk.PhotoImage(self.pil_image)
        self.image_window.create_image(300,300,image=self.image)

        # self.image_window.setPixmap(
        #     QtGui.QPixmap.fromImage(dicom_file_parser.get_qtimage())
        #     )

        # self.image_title_label.setText(
        #     f'Body Part: {dicom_file_parser.get_body_part_title()}')
        # self.image_number.setText(
        #     f'IMG # {dicom_file_parser.get_instance_number()}')
