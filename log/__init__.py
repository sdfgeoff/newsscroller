'''Logging is a good thing to have in any project. After playing with the python
default logger I got annoyed at how hard it was to configure. I also
wanted it to log the traceback (where it's being logged from) to help with
debugging, so I wrote my own logger.

This code does not import BGE so does not have to be GPL
'''
from .logger import Logger


def clear_file(path):
    '''Writes an empty string to the specified file'''
    open(path, 'w').write('')
