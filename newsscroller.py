#!/usr/bin/python3
import curses

import colors
import scheduler
import setting_file
import news


DEFAULT_SETINGS = {
    "sources": [
        {'type': 'rss', 'data': ["http://feeds.reuters.com/reuters/worldNews"]}
    ],
    "timings": {
        "between_characters": 0.01,
        "between_messages": 15,
        "between_updates": 300,
    },
    "max_from_each_feed": 10
}


def main(stdscr):
    '''Starts the program running'''
    stdscr.clear()
    setup_colors()
    sched = scheduler.Scheduler()
    settings = setting_file.SettingFile('settings.conf', DEFAULT_SETINGS)

    NewsScroller(stdscr, sched, settings)
    while 1:
        sched.update()


def setup_colors():
    '''Sets up curses colors'''
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(0, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(colors.GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(colors.CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(colors.RED, curses.COLOR_RED, curses.COLOR_BLACK)


class NewsScroller():
    '''Displays news on the screen, typing it out and then waiting, before
    typing out the next one'''
    def __init__(self, window, sched, settings):
        self.window = window  # A ncurses screen
        self.scheduler = sched  # A scheduler
        self.settings = settings  # Configuration

        self.news = news.NewsAggregator(
            settings['sources'],
            self.settings['max_from_each_feed']
        )

        self.type_event = scheduler.Event(
            self.type,
            time_between=settings['timings']['between_characters']
        )
        self.scheduler.register(self.type_event)

        self.between_event = scheduler.Event(
            self.next,
            time_between=settings['timings']['between_messages']
        )
        self.scheduler.register(self.between_event)

        self.refresh_news_event = scheduler.Event(
            self.news.update_all,
            time_between=settings['timings']['between_updates']
        )
        self.scheduler.register(self.refresh_news_event)

        self.current_article_id = 0
        self.current_article = None
        self.current_char_id = 0

        self.news.update_all()

    def type(self):
        '''puts the next character on the screen'''
        if self.current_article is None:
            self.next()

        data = "{:<40}{:>40}".format(
            self.current_article.source,
            self.current_article.time
        )
        title = self.current_article.title[:80].center(80, ' ')
        content = self.current_article.text
        col = self.current_article.color

        if self.current_char_id <= len(data):
            self.window.addstr(
                0, 0,
                data[:self.current_char_id],
                curses.color_pair(col)
            )
            self.window.refresh()
            self.current_char_id += 1
        elif self.current_char_id <= len(data) + len(title):
            self.window.addstr(
                1, 0,
                title[:self.current_char_id - len(data)],
                curses.color_pair(col) | curses.A_BOLD
            )
            self.window.refresh()
            self.current_char_id += 1
        elif self.current_char_id <= len(data) + len(title) + len(content):
            self.window.addstr(
                3, 0,
                content[:self.current_char_id - len(data) - len(title)],
                curses.color_pair(col)
            )
            self.window.refresh()
            self.current_char_id += 1

    def next(self):
        '''moves on to the next article'''
        self.window.clear()
        self.current_article_id += 1
        if self.current_article_id not in range(len(self.news.items)):
            self.current_article_id = 0
        self.current_article = self.news.items[self.current_article_id]
        self.current_char_id = 0

    def __del__(self):
        '''Removes all the stuff associated with this news scroller'''
        self.scheduler.remove(self.type_event)
        self.scheduler.remove(self.between_event)
        self.scheduler.remove(self.refresh_news_event)


if __name__ == "__main__":
    curses.wrapper(main)
