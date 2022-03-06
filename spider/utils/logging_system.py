"""logging_system"""

import os
import logging
import logging.handlers


class LoggingSystem(object):
    """
    hh
    """
    def __init__(self, _log_save_dir):
        self.log_save_dir = _log_save_dir
    # make a folder

    @staticmethod
    def mkdir(_path):
        """
        hh
        """
        _path = _path.strip()

        _path = _path.rstrip("\\")

        isExists = os.path.exists(_path)

        if not isExists:

            os.makedirs(_path)

            return True
        else:

            return False

    # logging system
    def ns_log(self, _log_file_name):

        """
        hh
        """

        # make a folder named by log_file_name to store log
        file_folder = self.log_save_dir + '/' + _log_file_name

        self.mkdir(file_folder)

        # initial a logger
        log = logging.getLogger(_log_file_name)
        log.setLevel(logging.DEBUG)

        # output to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # output to file
        file_handler = logging.handlers.TimedRotatingFileHandler(filename=file_folder + "/" + _log_file_name,
                                                                 when='midnight', delay=True)
        file_handler_error = logging.handlers.TimedRotatingFileHandler(filename=file_folder + "/" +_log_file_name+'_error',
                                                                 when='midnight', delay=True,)
        file_handler.setLevel(logging.DEBUG)
        file_handler_error.setLevel(logging.ERROR)

        # output format
        formatter = logging.Formatter('%(message)s\n')
        formatter_error = logging.Formatter('\n程序退出时间:%(asctime)s\n报错内容:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        file_handler_error.setFormatter(formatter_error)

        log.addHandler(file_handler)
        log.addHandler(console_handler)
        log.addHandler(file_handler_error)

        return log
