import json

import scrapy
from scrapy.crawler import CrawlerProcess

from Comment import Comment
from CsvHelper import CsvHelper


class CommentSpider(scrapy.Spider):
    # this spider scrapes a single article within the domain zeit.de
    name = 'zeit.de'
    urls = ['http://www.dailymail.co.uk/reader-comments/p/asset/readcomments/5014791?max=1000&order=desc&rcCache=shout']

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(
                url=str(url),
                callback=self.parse,
                method='GET',
                meta={'url': url}
            )

    def parse(self, response):
        if response.status is not 200:
            print('Response Code was {}'.format(response.status))
            return
        response_body = json.loads(response.text).get('payload')
        raw_comments = response_body.get('page')

        comments = []
        for raw_comment in raw_comments:
            comment = Comment(raw_comment)
            comments.append(comment)
            for reply in raw_comment.get('replies').get('comments'):
                reply = Comment(reply, comment.comment_id)
                comments.append(reply)
        CsvHelper.write_comments('comments.csv', comments)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'LOG_LEVEL': 'ERROR'
})

process.crawl(CommentSpider)
process.start()  # the script will block here until the crawling is finished
