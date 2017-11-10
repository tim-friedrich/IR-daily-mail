import csv

import os


class CsvHelper:
    @staticmethod
    def write_object_list(file_name: str, object_list):
        if not file_name.startswith('out/'):
            file_name = 'out/' + file_name

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
    def read_object_list(file_name: str, object_class):
        if not file_name.startswith('out/'):
            file_name = 'out/' + file_name

        if not os.path.isfile(file_name):
            raise FileNotFoundError('File {} does not exists'.format(file_name))
        with open(file_name, newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # skip header
            for row in reader:
                yield object_class(*row)

    @staticmethod
    def get_file_length(file_name):
        if not file_name.startswith('out/'):
            file_name = 'out/' + file_name

        if not os.path.isfile(file_name):
            raise FileNotFoundError('File {} does not exists'.format(file_name))

        with open(file_name, newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            file_length = sum(1 for row in reader)
        return file_length
