import time
import textwrap

class News():
    '''Represents a single news article for display'''
    def __init__(self, title, text, source, created_time, color=1):
        self.title = title
        self.text = textwrap.fill(text, 80)
        self.source = source
        self.time = time.strftime("Published %H:%M %d/%m/%y", created_time)
        self.color = color
