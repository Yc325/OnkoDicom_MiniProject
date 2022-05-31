"""Testing the dicom file parser model"""
from models import dicom_file_parser_model


def test_dicom_file_parser_model():
    """
    Creates a DicomFileParserModel instance
    """

    # WARNING: changing this example file will cause this test to fail
    example_dicom_image_path = "dicom_file/CT_183_Hashed.dcm"
    model = dicom_file_parser_model.DicomFileModel(example_dicom_image_path)

    assert model.get_instance_number() == 183
    assert model.get_qtimage() is not None
    assert model.get_type() == "CT Image"
    assert model.get_body_part_title() == "NECK"
