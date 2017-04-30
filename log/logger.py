'''The root class for the logger'''
import traceback


class Logger(object):
    '''The Logger logs output both to the console and to a file.
    It's instance in bge.log should be used in place of python's inbuild
    print function. Basic usage is:
    log = Logger(open('somefile', 'a'))
    log.info("Something that may help debugging")
    log.warn("Something non-fatal. Continuing")
    log.error("Something fatal, the game will likely not work")

    You pass in your own file_handle.
    The write method will be called, so make sure that (if it's a file) it is
    opened in append mode open(path, 'a')
    '''
    ERROR = 'ERROR: '
    WARN = 'WARN: '
    INFO = 'INFO: '

    def __init__(self, file_handle=None, display_function=print):
        self.file_handle = file_handle
        self.display_function = display_function

    def _out_to_file(self, out_str):
        '''Handles output to the actual file'''
        if self.file_handle is not None:
            self.file_handle.write(out_str + '\n')

    def log_raw(self, in_str):
        '''Writes a string as is to the file and prints it. Handles
        the formatting'''
        stack = traceback.extract_stack()[:-2]
        for entry in stack:
            if hasattr(entry, 'filename'):
                self._out_to_file("{}:{}".format(
                    entry.filename,
                    entry.lineno
                ))
            else:
                self._out_to_file("{}:{}".format(
                    entry[0],
                    entry[1]
                ))
        self._out_to_file(in_str + '\n')
        last = stack[-1]

        if hasattr(last, 'filename'):
            out_str = "{}:{}\n{}".format(last.filename, last.lineno, in_str)
        else:
            out_str = "{}:{}\n{}".format(last[0], last[1], in_str)
        if self.display_function is not None:
            self.display_function(out_str)
        return out_str

    def log_error(self, err):
        exc_type, exception, trace = err
        self.log_raw(''.join(traceback.format_exception(*err)))

    def info(self, in_str):
        '''Log something that is expected behaviour, but may help
        debugging, eg the progression of a loading system'''
        return self.log_raw(self.INFO + str(in_str))

    def warn(self, in_str):
        '''Log something that is not expected behaviour, but should
        not affect the running of the game.'''
        return self.log_raw(self.WARN + str(in_str))

    def error(self, in_str):
        '''Log something that is not expected behaviour and will
        likely cause the game to fail, eg missing shader files'''
        return self.log_raw(self.ERROR + str(in_str))
