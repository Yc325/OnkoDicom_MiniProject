import logging

class custLogger:
    def __init__(self, logLevel = logging.DEBUG, name=__name__):
        #create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logLevel)
        
        #create file handler and set the log level
        fh = logging.FileHandler("logFile.log")
        
        #create formater
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - : %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
        #add formatter to file handler
        fh.setFormatter(formatter)

        #add file handler to logger
        self.logger.addHandler(fh)