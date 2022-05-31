"""Testing the Confifuration class"""
from os.path import dirname
from models import configuration


def test_configuration():
    """
    Testing the configuration object which sets up the DB
    for storing the configuration settings
    """
    # WARNING: this needs to be called before the other tests
    # which rely on a default directory existing in the db
    config = configuration.Configuration()
    parent_directory = dirname(__file__).split("\\src")[0]
    config.update_default_dir(f"{parent_directory}\\dicom_file")
