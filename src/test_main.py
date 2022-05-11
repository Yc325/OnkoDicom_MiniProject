"""
Instantiating some classes
"""
from models import dicom_file_parser_model
from models import main_model


def test_main_model():
    """
    Creates a MainModel instance
    """
    model = main_model.MainModel()

    # uses setter methods
    model.selected_dicom_directory = "new_dicom_directory"
    model.selected_image_file_path = "new_image_file_path"

    # tests getter methods
    assert model.selected_dicom_directory == "new_dicom_directory"
    assert model.selected_image_file_path == "new_image_file_path"


def test_dicom_file_parser_model():
    """
    Creates a DicomFileParserModel instance
    """

    # WARNING: changing this example file will cause this test to fail
    example_dicom_image_path = "dicom_file/CT_183_Hashed.dcm"
    model = dicom_file_parser_model.DicomFileModel(example_dicom_image_path)

    assert model.get_image_number() == 183
    assert model.get_dataset() is not None
    assert model.get_body_part_title() == "NECK"
