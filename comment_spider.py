import json

import scrapy
from scrapy import Spider, Request

from comment import Comment
from csv_helper import CsvHelper

URL_TEMPLATE = 'http://www.dailymail.co.uk/reader-comments/p/asset/readcomments/{}?max=1000&order=desc&rcCache=shout&offset={}'
MAX_COMMENTS = 1000


class CommentSpider(Spider):
    name = 'dailymail.co.uk'
    urls = [
        'http://www.dailymail.co.uk/reader-comments/p/asset/readcomments/5036717?max=1000&order=desc&rcCache=shout&offset=0']

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

        response_data = json.loads(response.text).get('payload')
        raw_comments = response_data.get('page')
        comments = []
        for raw_comment in raw_comments:
            comment = Comment(raw_comment)
            comments.append(comment)
            for reply in raw_comment.get('replies').get('comments'):
                reply = Comment(reply, comment.comment_id)
                comments.append(reply)
        CsvHelper.write_comments('comments.csv', comments)
        offset = int(response_data.get('offset'))

        if offset + MAX_COMMENTS < response_data.get('parentCommentsCount'):
            offset += 1000
            print(offset)
            yield scrapy.Request(URL_TEMPLATE.format(response_data.get('assetId'), offset), self.parse)
