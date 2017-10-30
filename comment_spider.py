import json

from scrapy import Spider, Request

from comment import Comment
from csv_helper import CsvHelper


class CommentSpider(Spider):
    name = 'dailymail.co.uk'
    urls = ['http://www.dailymail.co.uk/reader-comments/p/asset/readcomments/4984538?max=1000&order=desc&rcCache=shout']

    def start_requests(self):
        for url in self.urls:
            yield Request(
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
