from datetime import date

import os
from shutil import copyfile

from constants import ARTICLES_FILE_NAME_TEMPLATE, OUT_DIR


class Article:
    def __init__(self, article_id, article_url, article_date):
        self.article_id = article_id
        self.article_url = article_url
        self.date = article_date

    @staticmethod
    def get_csv_file_name():
        return ARTICLES_FILE_NAME_TEMPLATE.format(date.today().strftime('%Y%m%d'))

    @staticmethod
    def copy_last_article_file():
        latest_file = Article.get_latest_file()
        if latest_file:
            copyfile(latest_file, Article.get_csv_file_name())

    @staticmethod
    def get_latest_file():
        article_files = [file for file in os.listdir(OUT_DIR) if file.startswith('articles-')]
        if not article_files:
            return ''
        latest_file = sorted(article_files)[-1]
        return latest_file
