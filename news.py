import time
import textwrap
import random
import html
import re

import sources


class News():
    '''Represents a single news article for display'''
    def __init__(self, title, text, source, created_time, color=1):
        self.title = title
        self.text = textwrap.fill(html.unescape(text), 79)
        self.source = source
        if created_time is not None:
            self.time = time.strftime("Published %H:%M %d/%m/%y", created_time)
        else:
            self.time = None
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
            news_items = source.update()
            for news_item in news_items:
                if self.is_relevant(news_item, source.keywords):
                    self.items.append(news_item)
                # Prevent there being too many news items
                if source.max is not None:
                    if len(self.items) >= source.max:
                        break
                if len(self.items) >= self.max_items_per_source:
                    break
        random.shuffle(self.items)

    def is_relevant(self, news_item, keyword_list):
        '''Returns 'True' if the source looks relevant based on keywords'''
        if keyword_list == [] or keyword_list is None:
            return True
        keyword_str = ""
        for keyword in keyword_list:
            keyword_str += keyword + "|"
        regex = re.compile("(({})\s)+".format(keyword_str[:-1]), re.IGNORECASE)
        return regex.fullmatch(news_item.title) or regex.fullmatch(news_item.text)
