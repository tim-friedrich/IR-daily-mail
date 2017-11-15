import os
from datetime import date
from shutil import copyfile

from constants import ARTICLES_FILE_NAME_TEMPLATE, COMMENTS_FILE_NAME_TEMPLATE, OUT_DIR


class ModelHelper:
    class Meta:
        abstract = True

    def get_csv_file_name(self, file_name_template: str):
        return file_name_template.format(date.today().strftime('%Y%m%d'))

    def get_latest_file(self, file_prefix: str):
        files = [file for file in os.listdir(OUT_DIR) if file.startswith(file_prefix)]
        if not files:
            return ''
        latest_file = sorted(files)[-1]
        return latest_file


class ArticlesHelper(ModelHelper):
    def get_csv_file_name(self, **kwargs):
        return super().get_csv_file_name(ARTICLES_FILE_NAME_TEMPLATE)

    def get_latest_file(self, **kwargs):
        return super().get_latest_file('articles-')

    def copy_last_article_file(self):
        latest_file = self.get_latest_file()
        if latest_file:
            copyfile(OUT_DIR + latest_file, OUT_DIR + self.get_csv_file_name())


class CommentsHelper(ModelHelper):
    def get_csv_file_name(self, **kwargs):
        return super().get_csv_file_name(COMMENTS_FILE_NAME_TEMPLATE)

    def get_latest_file(self, **kwargs):
        return super().get_latest_file('comments-')
