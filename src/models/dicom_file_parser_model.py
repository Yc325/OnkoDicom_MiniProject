"""
Declares DicomFile model for wrapping a dicom file path
and having easier accessibility
"""
# pylint: disable=E1101
# pylint: disable=C0413
# pylint: disable=C0411
import sys
import numpy as np
import pydicom
from PySide6 import QtGui
from custom_logging.logger import CustLogger

# WARNING: this is required because of ImageQt backend issues
# need to clean up our imports/dependencies as it is very fragile
sys.modules['PyQt6.QtGui'] = QtGui
from PIL import Image, ImageQt  # noqa: E402

# call logging
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

        try:
            self.body_part_title = dataset['BodyPartExamined'].value
            self.instance_number = dataset['InstanceNumber'].value
        except KeyError:
            self.body_part_title = ""
            self.instance_number = 0

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

        arr = dataset.pixel_array.astype(float)
        rescaled_im = (np.maximum(arr, 0) / arr.max()) * 255
        final_image = np.uint8(rescaled_im)
        pillow_image = Image.fromarray(final_image)

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
        logging_display.logger.warning("Does not support this file type: %s",
                                       class_uid)
        return False
