import logging


class Logger:
    _instance = None
    _initialized = False
    
    def __new__(cls, log_file=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, log_file=None):
        if not Logger._initialized:
            self.log_file = log_file
            logging.basicConfig(
                filename=self.log_file,
                format = '%(message)s',
                filemode = 'w',
            )

            self.logger = logging.getLogger()
            self.logger.setLevel(logging.DEBUG)
            Logger._initialized = True

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


    def change_log_file(self, log_file):
        self.log_file = log_file
        logging.basicConfig(
            filename=self.log_file,
            format = '%(message)s',
            filemode = 'w',
        )
        self.logger.info(f"Log file changed to {log_file}")

