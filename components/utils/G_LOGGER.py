import logging, logging.handlers
import os

class G_LOGGER:
    def __init__(self,part,sub_part=None):
        self.part = part
        self.sub_part = sub_part

    def get_logger(self):
        # create logger with 'spam_application'
        logger = logging.getLogger(f"{self.part}.{self.sub_part}")
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.handlers.RotatingFileHandler(f"logs//{self.part}.{self.sub_part}.log",mode='w',maxBytes=20000,backupCount=4)
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger


if __name__ == "__main__":
    x = os.path()
    print(x)