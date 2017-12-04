import csv
import os
from io import StringIO
from typing import Type

from models.comment import Comment
from models.csv_model import CsvItem
from utils import check_file_name


class CsvHelper:
    def __init__(self, file_name: str):
        self.file_name = file_name

    def write_object_list(self, object_list: [CsvItem]):
        file_name = check_file_name(self.file_name)

        if not object_list:
            return

        file_exists = os.path.isfile(file_name)
        with open(file_name, newline='', mode='a', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, object_list[0].__class__.get_members(), quoting=csv.QUOTE_ALL)
            if not file_exists:
                writer.writeheader()

            for element in object_list:  # type: CsvItem
                position = csv_file.tell()
                writer.writerow(element.get_dict())
                length = csv_file.tell() - position
                element.pointer = position
                element.length = length
        return object_list

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
