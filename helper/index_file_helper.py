import logging
import pickle

import xdelta3

from constants import OUT_DIR
from models.index import Index


class IndexFileHelper:
    @property
    def posting_file(self):
        return OUT_DIR + 'posting_list'

    @property
    def compressed_postings(self):
        return OUT_DIR + 'posting_list.comp'

    @property
    def index_file(self):
        return OUT_DIR + 'index.pkl'

    def write_posting_list(self, posting_list: list, index: Index):
        pointer_index = Index(index.get_file())
        with open(self.posting_file, mode='w', encoding='utf-8') as file:
            counter = 0
            for row in posting_list:
                start = file.tell()
                file.write(row + '\n')
                end = file.tell()
                for key, value in index.items():
                    if value == counter:
                        pointer_index[key] = [start, end]
                        del index[key]
                        break
                counter += 1
        return pointer_index

    def get_posting(self, start, end):
        with open(self.posting_file, mode='rb') as file:
            file.seek(start)
            row = file.read(end - start).decode()
        return row.split(',')

    def write_index(self, index: dict):
        with open(self.index_file, 'wb') as output:
            pickle.dump(index, output, pickle.HIGHEST_PROTOCOL)

    def get_index(self):
        with open(self.index_file, 'rb') as file:
            return pickle.load(file)

    def compress_index(self, file_name):
        logging.info('Compressing {}'.format(file_name))
        with open(file_name, mode='rb') as file:
            with open(file_name + '.comp', mode='wb+') as compressed_file:
                previous_line = ''
                for line in file:
                    if not previous_line:
                        previous_line = line
                        encoded_line = line
                    else:
                        try:
                            encoded_line = xdelta3.encode(previous_line, line)
                        except xdelta3.NoDeltaFound:
                            encoded_line = line
                    compressed_file.write(encoded_line)
