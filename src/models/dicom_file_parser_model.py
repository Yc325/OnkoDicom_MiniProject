"""
Declares DicomFile model for wrapping a dicom file path
and having easier accessibility
"""
import pydicom

class DicomFileModel:
    """
    A model class that handles all the processing of the dicom files
    """
    def __init__(self, path):
        dataset = pydicom.dcmread(path)

        all_tags = ''
        for elem in dataset:
            tag = str(elem) + '\n'
            all_tags += tag

        self.dataset = dataset
        self.all_tags = all_tags
        self.body_part_title = dataset['BodyPartExamined'].value
        self.image_number = dataset['InstanceNumber'].value

    def get_image_number(self):
        """Gets the image number"""
        return self.image_number

    def get_body_part_title(self):
        """Gets the body part title"""
        return self.body_part_title

    def get_dataset(self):
        """Gets the dataset"""
        return self.dataset
