import time
import textwrap

import sources
import random


class News():
    '''Represents a single news article for display'''
    def __init__(self, title, text, source, created_time, color=1):
        self.title = title
        self.text = textwrap.fill(text, 79)
        self.source = source
        self.time = time.strftime("Published %H:%M %d/%m/%y", created_time)
        self.color = color


class NewsAggregator():
    '''Collects news from a variety of sources as defined by an input list'''
    def __init__(self, source_list, max_items_per_source):
        self._raw_sources = source_list
        self.sources = list()
        self.max_items_per_source = max_items_per_source
        self.init_all()
        self.update_all()
        self.items = list()

    def init_all(self):
        '''Initilizes each source'''
        for source in self._raw_sources:
            source_type = sources.SOURCE_TABLE[source['type']]
            self.sources.append(source_type(*source['data']))

    def update_all(self):
        '''Refreshes all news sources'''
        self.items = list()
        for source in self.sources:
            self.items += source.update()[:self.max_items_per_source]
        random.shuffle(self.items)
