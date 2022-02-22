import time
import logging

def timeit(f):
    def timed(*args, **kw):

        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        print(f"Finish function : {f.__name__}{args} after {te-ts} seconds.")
        return result

    return timed

def convert_bytes(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0

    return size

def mute_third_party_logger():
    for log_name, log_obj in logging.Logger.manager.loggerDict.items():
        if log_name != __name__:
            log_obj.disabled = True