#!/usr/bin/python3
import feedparser
import curses
import random

import sources
import colors
import scheduler


MAX_FROM_EACH_FEED = 10
SOURCE_LIST = [
	#"http://feeds.bbci.co.uk/news/world/rss.xml",
    {'type':'rss', 'data':["http://feeds.reuters.com/reuters/worldNews"]}
]

def setup_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(0, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(colors.GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(colors.CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(colors.RED, curses.COLOR_RED, curses.COLOR_BLACK)

def generate_news_list(source_list):
    news_items = list()
    feedparser._HTMLSanitizer.acceptable_elements = []
    for item in source_list:
        instance = sources.SOURCE_TABLE[item['type']](*item['data'])
        news_items += instance.update()[:MAX_FROM_EACH_FEED]

    random.shuffle(news_items)
    return news_items


class NewsScroller():
    def __init__(self, window, source_list, sched, type_delay, between_delay, refresh_news_delay):
        self.window = window  # A ncurses screen
        self.source_list = source_list  # A list of urls to get news from
        self.scheduler = sched  # A scheduler that can be used to register events

        self.type_event = scheduler.Event(self.type, time_between=type_delay)
        self.between_event = scheduler.Event(self.next, time_between=between_delay)
        self.refresh_news_event = scheduler.Event(self.refresh_news, time_between=refresh_news_delay)

        self.scheduler.register(self.type_event)
        self.scheduler.register(self.between_event)
        self.scheduler.register(self.refresh_news_event)

        self.news = list()
        self.current_article_id = 0
        self.current_article = None
        self.current_char_id = 0
        self.refresh_news()
        self.next()

    def type(self):
        '''puts the next character on the screen'''
        if self.current_article == None:
            self.next()

        data = "{:<40}{:>40}".format(self.current_article.source, self.current_article.time)
        title = self.current_article.title[:80].center(80, ' ')
        content = self.current_article.text
        col = self.current_article.color

        news_str = title
        if self.current_char_id <= len(data):
            self.window.addstr(0, 0, data[:self.current_char_id], curses.color_pair(col))
            self.window.refresh()
            self.current_char_id += 1
        elif self.current_char_id <= len(data) + len(title):
            self.window.addstr(1, 0, title[:self.current_char_id - len(data)], curses.color_pair(col) | curses.A_BOLD)
            self.window.refresh()
            self.current_char_id += 1
        elif self.current_char_id <= len(data) + len(title) + len(content):
            self.window.addstr(3, 0, content[:self.current_char_id - len(data) - len(title)], curses.color_pair(col))
            self.window.refresh()
            self.current_char_id += 1

    def next(self):
        '''moves on to the next article'''
        self.window.clear()
        self.current_article_id += 1
        if self.current_article_id not in range(len(self.news)):
            self.current_article_id = 0
        self.current_article = self.news[self.current_article_id]
        self.current_char_id = 0

    def refresh_news(self):
        '''Retches news from the news sources'''
        self.news = generate_news_list(self.source_list)


def main(stdscr):
    stdscr.clear()
    setup_colors()
    sched = scheduler.Scheduler()
    NewsScroller(stdscr, SOURCE_LIST, sched, 0.01, 15, 300)
    while(1):
        sched.update()
    #while(1):
    #    news_list = generate_news_list(source_list)
    #    for item in news_list:
    #        stdscr.addstr(0, 0, item.title, curses.A_BOLD | curses.color_pair(1))
    #        stdscr.addstr(1,1, item.summary, curses.color_pair(2))
    #        stdscr.refresh()
    #    time.sleep(10)


if __name__ == "__main__":
    curses.wrapper(main)
