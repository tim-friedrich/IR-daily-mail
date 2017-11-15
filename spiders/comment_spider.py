import json
from json import JSONDecodeError

import scrapy
from scrapy import Spider, Request

from constants import MAX_COMMENTS, COMMENTS_URL_TEMPLATE
from helper.csv_helper import CsvHelper
from helper.model_helper import ArticlesHelper, CommentsHelper
from models.article import Article
from models.comment import Comment


class CommentSpider(Spider):
    name = 'dailymail comments'

    def __init__(self, **kwargs):
        self.articles_helper = ArticlesHelper()
        self.comments_helper = CommentsHelper()
        super().__init__(**kwargs)

    def start_requests(self):
        for article in CsvHelper.read_object_list(self.articles_helper.get_latest_file(), Article):
            url = COMMENTS_URL_TEMPLATE.format(article.article_id, 0)
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
        try:
            response_data = json.loads(response.text).get('payload')
            raw_comments = response_data.get('page')
            comments = []
            for raw_comment in raw_comments:
                comment = Comment(raw_comment)
                comments.append(comment)
                for reply in raw_comment.get('replies').get('comments'):
                    reply = Comment(reply, comment.comment_id)
                    comments.append(reply)

            CsvHelper.write_object_list(self.comments_helper.get_csv_file_name(), comments)

            # find all comments if article has more than 1000
            offset = int(response_data.get('offset'))
            if offset + MAX_COMMENTS < response_data.get('parentCommentsCount'):
                offset += 1000
                yield scrapy.Request(COMMENTS_URL_TEMPLATE.format(response_data.get('assetId'), offset), self.parse)

        except AttributeError as e:
            print('AttributeError: {}. Response: {}'.format(e, response.text))
        except JSONDecodeError as e:
            print('JSONError: {}. Response: {}'.format(e, response.text))
