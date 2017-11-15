import csv
import linecache
import os
from io import StringIO
from typing import Type

import pandas

from constants import OUT_DIR
from helper.model_helper import CommentsHelper
from models.comment import Comment
from models.csv_model import CsvModel
from utils import check_file_name


class CsvHelper:
    @staticmethod
    def write_object_list(file_name: str, object_list):
        file_name = check_file_name(file_name)

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

    @staticmethod
    def read_object_list(file_name: str, object_class: Type[CsvModel]):
        file_name = check_file_name(file_name)

        if not os.path.isfile(file_name):
            raise FileNotFoundError('File {} does not exists'.format(file_name))
        with open(file_name, newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, )
            headers = next(reader)
            if not headers == object_class.get_members():
                raise AttributeError('Different rows than members')
            line = 1
            for row in reader:
                yield object_class.parse_csv_row(row, line)
                line += 1

    @staticmethod
    def read_comment(line: int):
        file = OUT_DIR + CommentsHelper().get_latest_file()
        data_frame = pandas.read_csv(file, header=None, skiprows=line, nrows=1)
        comment = Comment.parse_csv_row(list(data_frame.get_values()[0]), line)
        return comment

    @staticmethod
    def read_comment_linecache(line: int):
        file = OUT_DIR + CommentsHelper().get_latest_file()
        row = linecache.getline(file, line)
        csv_row = next(csv.reader(StringIO(row)))
        comment = Comment.parse_csv_row(csv_row, line)

        return comment

    @staticmethod
    def get_file_length(file_name):
        file_name = check_file_name(file_name)

        if not os.path.isfile(file_name):
            raise FileNotFoundError('File {} does not exists'.format(file_name))

        with open(file_name, newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            file_length = sum(1 for _ in reader)
        return file_length
