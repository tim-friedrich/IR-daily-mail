import logging

from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import TweetTokenizer

from helper.csv_helper import CsvHelper
from helper.index_file_helper import IndexFileHelper
from helper.model_helper import CommentsHelper
from models.comment import Comment


class CommentsIndex:
    def __init__(self):
        self.stemmer = SnowballStemmer("english")
        self.tokenizer = TweetTokenizer()
        self.helper = IndexFileHelper()
        self.index = dict()
        self.restore_index()

    def __del__(self):
        self.helper.write_index(self.index)

    def restore_index(self):
        try:
            self.index = self.helper.get_index()
        except FileNotFoundError:
            logging.info('No previous index was found. Creating new one.')
            self.build_index()

    def search(self, query: str, number_of_results: int):
        if len(query.split(' ')) > 1:
            raise AttributeError('Only single word query\'s are supported for now')
        processed_query = self.get_tokens(query)
        results = list()
        for token in processed_query:
            posting_pointer = self.index.get(token)
            if not posting_pointer:
                continue
            i = 0
            for posting in self.helper.get_posting(posting_pointer[0], posting_pointer[1]):
                comment = CsvHelper.read_comment(CommentsHelper().get_latest_file(), *posting.split(';'))
                results.append(comment)
                if i > number_of_results:
                    break
                i += 1

        return results

    def build_index(self):
        comments_file = CommentsHelper().get_latest_file()
        self.index = dict()

        logging.info('Comments to index: ' + str(CsvHelper.get_file_length(comments_file) - 1))
        counter = 0
        posting_list = []
        for comment in CsvHelper.read_object_list(comments_file, Comment):  # type: Comment
            for token in self.get_tokens(comment.comment_text):
                posting_list_pointer = self.index.get(token)  # type: int
                posting = '{};{}'.format(comment.pointer, comment.length)
                if posting_list_pointer is not None:
                    posting_list[posting_list_pointer] += ',' + posting
                else:
                    posting_list.append(posting)
                    self.index[token] = len(posting_list) - 1

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
