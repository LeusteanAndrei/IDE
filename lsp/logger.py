import logging


class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        logging.basicConfig(
            filename=self.log_file,
            format = '%(message)s',
            filemode = 'w',
        )

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
