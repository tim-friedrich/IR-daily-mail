import logging

from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import TweetTokenizer

from helper.csv_helper import CsvHelper
from helper.index_file_helper import IndexFileHelper
from helper.model_helper import CommentsHelper
from models.comment import Comment
from models.index import Index
from vsm import VSM


class CommentsIndex:
    def __init__(self, rebuild_index=False):
        self.index = Index(CommentsHelper().get_latest_file())
        self.stemmer = SnowballStemmer("english")
        self.tokenizer = TweetTokenizer()
        self.helper = IndexFileHelper()
        self.vsm = VSM(self, rebuild_index)

        if rebuild_index:
            self.build_index()
        else:
            self.restore_index()

    def __del__(self):
        self.helper.write_index(self.index)

    def restore_index(self):
        try:
            self.index = self.helper.get_index()
            if self.index.get_file() != CommentsHelper().get_latest_file():
                logging.debug(
                    'Restored index based on {}. To create the index of last file use attribute "index".'.format(
                        self.index.get_file()))
        except FileNotFoundError:
            logging.info('No previous index was found. Creating new one.')
            self.build_index()

    def build_index(self):
        logging.info('Comments to index: ' + str(CsvHelper.get_file_length(self.index.get_file()) - 1))
        counter = 0
        posting_list = []
        for comment in CsvHelper.read_object_list(self.index.get_file(), Comment):  # type: Comment
            token_position = 0
            for token in self.get_tokens(comment.comment_text):
                self.vsm.add_term(comment.comment_id, token)
                posting_list_pointer = self.index.get(token)  # type: int
                posting = '{};{};{}'.format(comment.pointer, comment.length, token_position)
                if posting_list_pointer is not None:
                    posting_list[posting_list_pointer] += ',' + posting
                else:
                    posting_list.append(posting)
                    self.index[token] = len(posting_list) - 1
                token_position += 1
            counter += 1
            print('\rComments indexed: ' + '{:,}'.format(counter), end='')
        self.index = self.helper.write_posting_list(posting_list, self.index)

    def get_tokens(self, comment):
        comment = self.normalize(comment)
        tokens = self.tokenizer.tokenize(comment)
        processed_tokens = []
        for token in tokens:
            token = self.stem(token)
            if token != '':
                processed_tokens.append(token)
        return processed_tokens

    def stem(self, token):
        return self.stemmer.stem(token)

    def normalize(self, token):
        puncts = '.?!,"%'
        token = token.lower()
        for sym in puncts:
            token = token.replace(sym, '')
        return token

    def get_postings(self, token, use_wildcard=False):
        if use_wildcard:
            postings = []
            for pointer in self.index.get_starts_with(token):
                for posting in self.helper.get_posting(*pointer):
                    if not posting in postings:
                        postings.append(posting)
            return postings
        posting_pointer = self.index.get(token)
        if not posting_pointer:
            return []
        return self.helper.get_posting(*posting_pointer)
