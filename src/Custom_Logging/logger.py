"""
Established CustLogger class
"""
import logging
# pylint: disable = R0903


class CustLogger:
    """
    Call __init__
    """
    def __init__(self, log_level=logging.DEBUG, name=__name__):
        # create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        # create file handler and set the log level
        file_holder = logging.FileHandler("src/log_file.log")
        # create formater
        formatter = logging.Formatter('%(asctime)s '
                                      '- %(levelname)s '
                                      '- %(name)s '
                                      '- : %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')
        # add formatter to file handler
        file_holder.setFormatter(formatter)

        # add file handler to logger
        self.logger.addHandler(file_holder)
