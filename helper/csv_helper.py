import csv
import os
from io import StringIO
from typing import Type

from constants import OUT_DIR
from models.comment import Comment
from models.csv_model import CsvItem
from utils import check_file_name


class CsvHelper:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.authors = {}
        self.articles = {}
        self.last_author_id = 0

    def write_object_list(self, object_list):
        file_name = check_file_name(self.file_name)

        object_list = [element.__dict__ for element in object_list]
        if not object_list:
            return

        file_exists = os.path.isfile(file_name)
        with open(file_name, newline='', mode='a', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, object_list[0].keys(), quoting=csv.QUOTE_ALL)
            if not file_exists:
                writer.writeheader()

            for element in object_list:
                writer.writerow(element)

    def write_comments(self, comments_list):
        DIR = os.path.join(OUT_DIR, self.file_name)
        if not os.path.exists(DIR):
            os.mkdir(DIR)
        comments_file_name = os.path.join(DIR, 'comment.csv')
        articles_file_name = os.path.join(DIR, 'articles.csv')
        authors_file_name = os.path.join(DIR, 'authors.csv')

        comments_exits = os.path.isfile(comments_file_name)
        articles_exits = os.path.isfile(articles_file_name)
        authors_exits = os.path.isfile(authors_file_name)

        with open(comments_file_name, newline='', mode='a', encoding='utf-8') as comments_file:
            comments_writer = csv.DictWriter(comments_file,
                                             ['comment_id', 'article_id', 'comment_author_id', 'comment_text',
                                              'timestamp', 'parent_comment_id', 'upvotes', 'downvotes'],
                                             quoting=csv.QUOTE_ALL)
            if not comments_exits:
                comments_writer.writeheader()
            with open(articles_file_name, newline='', mode='a', encoding='utf-8') as articles_file:
                articles_writer = csv.DictWriter(articles_file, ['article_id', 'article_url'], quoting=csv.QUOTE_ALL)
                if not articles_exits:
                    articles_writer.writeheader()
                with open(authors_file_name, newline='', mode='a', encoding='utf-8') as authors_file:
                    authors_writer = csv.DictWriter(authors_file, ['comment_author_id', 'comment_author'],
                                                    quoting=csv.QUOTE_ALL)
                    if not authors_exits:
                        authors_writer.writeheader()

                    for comment in comments_list:
                        if not self.authors.get(comment.comment_author):
                            authors_writer.writerow({'comment_author_id': self.last_author_id,
                                                     'comment_author': comment.comment_author})
                            self.authors[comment.comment_author] = self.last_author_id
                            self.last_author_id += 1

                        if not self.articles.get(comment.article_id):
                            articles_writer.writerow({'article_id': comment.comment_id,
                                                      'article_url': comment.article_url})
                            self.articles[comment.article_id] = True

                        comments_writer.writerow({'comment_id': comment.comment_id,
                                                  'article_id': comment.article_id,
                                                  'comment_author_id': self.authors.get(comment.comment_author),
                                                  'comment_text': comment.comment_text,
                                                  'timestamp': comment.timestamp,
                                                  'parent_comment_id': comment.parent_comment_id,
                                                  'upvotes': comment.up_votes,
                                                  'downvotes': comment.down_votes})

    @staticmethod
    def read_object_list(file_name: str, object_class: Type[CsvItem]):
        file_name = check_file_name(file_name)

        if not os.path.isfile(file_name):
            raise FileNotFoundError('File {} does not exists'.format(file_name))
        with open(file_name, mode='rb') as csv_file:

            next(csv_file)  # skip header
            position = csv_file.tell()
            line = csv_file.readline()
            while line:
                line_length = csv_file.tell() - position
                data = next(csv.reader(StringIO(line.decode().rstrip())))

                yield object_class.parse_csv_row(data, position, line_length)
                position += line_length
                line = csv_file.readline()

    @staticmethod
    def read_comment(file_name, pointer, length, token_position=None):
        file_name = check_file_name(file_name)

        if not os.path.isfile(file_name):
            raise FileNotFoundError('File {} does not exists'.format(file_name))

        with open(file_name, mode='rb') as csv_file:
            csv_file.seek(int(pointer))
            line = csv_file.read(int(length))
            data = next(csv.reader(StringIO(line.decode().rstrip())))
            return Comment.parse_csv_row(data, token_position=token_position)

    @staticmethod
    def get_file_length(file_name):
        file_name = check_file_name(file_name)

        if not os.path.isfile(file_name):
            raise FileNotFoundError('File {} does not exists'.format(file_name))

        with open(file_name, newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            file_length = sum(1 for _ in reader)
        return file_length
