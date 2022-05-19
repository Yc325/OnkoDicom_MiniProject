"""
Declares DicomFile model for wrapping a dicom file path
and having easier accessibility
"""
# pylint: disable=E1101
# pylint: disable=C0413
import sys
import numpy as np
import pydicom
from PySide6 import QtGui
# WARNING: this is required because of ImageQt backend issues
# need to clean up our imports/dependencies as it is very fragile
sys.modules['PyQt6.QtGui'] = QtGui
from PIL import Image, ImageQt  # noqa: E402
from Custom_Logging.logger import CustLogger

#call logging
logging_display = CustLogger(name=__name__)

class DicomFileModel:
    """
    A model class that handles all the processing of the dicom files
    """
    # display logging info
    logging_display.logger.info('Class created')
    def __init__(self, path):
        dataset = pydicom.dcmread(path)

        all_tags = ''
        for elem in dataset:
            tag = str(elem) + '\n'
            all_tags += tag

        self.dataset = dataset
        self.all_tags = all_tags
        self.body_part_title = dataset['BodyPartExamined'].value
        self.instance_number = dataset['InstanceNumber'].value

    def get_instance_number(self):
        """Gets the file instance number"""
        # display logging info
        logging_display.logger.info('get_instance_number function called')
        return self.instance_number

    def get_body_part_title(self):
        """Gets the body part title"""
        # display logging info
        logging_display.logger.info('get_body_part_title function called')
        return self.body_part_title

    def get_qtimage(self):
        """Gets the qt_image"""
        # display logging info
        logging_display.logger.info('get_qtimage function called')
        # Try turn pixel data into image
        # from
        # https://github.com/pydicom/contrib-pydicom/blob/master/viewers/pydicom_PIL.py
        dataset = self.dataset

        win_width = dataset['WindowWidth']
        win_center = dataset['WindowCenter']

        if (win_width is None) or (win_center is None) or (dataset is None):
            logging_display.logger.error("Values win_width & win_center: %s %s"
                                         , win_width
                                         , win_center)


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

        return ImageQt.ImageQt(pillow_image)

    # move this function somewhere more relevent
    def get_type(self):
        """
        Returns the type of data contained within a DICOM file
        :return: type, string type of data in DICOM file
        """
        # display logging info
        logging_display.logger.info('get_type function called')
        elements = {
            '1.2.840.10008.5.1.4.1.1.481.3': "RT Struct",
            '1.2.840.10008.5.1.4.1.1.2': "CT Image",
            '1.2.840.10008.5.1.4.1.1.481.2': "RT Dose",
            '1.2.840.10008.5.1.4.1.1.481.5': "RT Plan"
        }

        class_uid = self.dataset["SOPClassUID"].value
        # Check to see what type of data the given DICOM file holds
        if class_uid in elements:
            return elements[class_uid]
        logging_display.logger.warning("Does not support this file type: %s"
                                       , class_uid)
        return False
