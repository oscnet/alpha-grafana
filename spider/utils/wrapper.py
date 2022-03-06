"""useful wrapper"""

import time
from functools import wraps
import traceback
import datetime


def retry(_retry_times, _sleep_seconds):
    """

    :param _retry_times:
    :param _log:
    :param _sleep_seconds:
    :return:
    """

    def retry_wrapper(func):
        """

        :param func:
        :return:
        """

        @wraps(func)
        def retry_func(*args, **kwargs):
            """
            :return:
            """
            error_info = str
            try:

                for _ in range(_retry_times):
                    try:
                        result = func(*args, **kwargs)
                        return result
                    except Exception:
                        error_info = '\n' + traceback.format_exc()
                        print(error_info)

                        time.sleep(_sleep_seconds)

                else:

                    raise ValueError(f'{datetime.datetime.now()}{func.__name__} 函数重试次数超过上限:{_retry_times}次，程序退出。')

            except Exception as e:
                print(e)
                print(error_info)

        return retry_func

    return retry_wrapper
