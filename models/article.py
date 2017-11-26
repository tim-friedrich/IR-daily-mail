import re

from models.csv_model import CsvItem


class Article(CsvItem):
    def __init__(self, article_url=None, article_date=None):
        if article_url and article_date:
            self.article_id = re.search('(?<=article-)\w*', article_url).group()
            self.date = article_date

    @staticmethod
    def get_members():
        return [
            'article_id',
            'date'
        ]
