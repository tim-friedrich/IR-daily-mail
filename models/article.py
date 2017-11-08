import re
from datetime import date

from constants import ARTICLES_FILE_NAME_TEMPLATE


class Article:
    def __init__(self, article_url, date):
        self.article_id = re.search('(?<=article-)\w*', article_url).group()
        self.article_url = article_url
        self.date = date

    @staticmethod
    def get_csv_file_name():
        return ARTICLES_FILE_NAME_TEMPLATE.format(date.today().strftime('%Y%m%d'))
