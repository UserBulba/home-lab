import logging


class Logger:
    def __init__(self, name, level=logging.INFO):
        """Logger - initialize logger"""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s]: %(message)s", "%H:%M:%S"
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        """get_logger - returns logger"""
        return self.logger

    def get_severity(self):
        """get_severity - returns severity level"""
        return self.logger.getEffectiveLevel()
