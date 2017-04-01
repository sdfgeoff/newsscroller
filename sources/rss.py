import feedparser

import news
import colors

class RSS(object):
    def __init__(self, url):
        self.url = url

    def update(self):
        '''Returns a list of news items'''
        news_items = list()
        feedparser._HTMLSanitizer.acceptable_elements = []
        data = feedparser.parse(self.url)
        for entry in data['entries']:
            created_time = None
            if 'created_parsed' in entry:
                created_time = entry.created_parsed
            elif 'published_parsed' in entry:
                created_time = entry.published_parsed
            new = news.News(
                entry.title,
                entry.summary,
                data.channel.title,
                created_time,
                color=colors.GREEN
            )
            news_items.append(new)

        return news_items



if __name__ == '__main__':
    print(RSS("http://feeds.bbci.co.uk/news/world/rss.xml").update())
