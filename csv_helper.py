import csv

import os


class CsvHelper:
    @staticmethod
    def write_object_list(file_name: str, object_list):
        if not file_name.startswith('out/'):
            file_name = 'out/' + file_name

        object_list = [object.__dict__ for object in object_list]
        if not object_list:
            return

        file_exists = os.path.isfile(file_name)
        with open(file_name, newline='', mode='a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, object_list[0].keys(), quoting=csv.QUOTE_ALL)
            if not file_exists:
                writer.writeheader()

            for object in object_list:
                writer.writerow(object)
