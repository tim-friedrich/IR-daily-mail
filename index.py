import pickle

from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import TweetTokenizer

from helper.csv_helper import CsvHelper
from models.comment import Comment


class CommentsIndex:
    def __init__(self):
        self.stemmer = SnowballStemmer("english")
        self.tokenizer = TweetTokenizer()
        self.index = dict()
        self.restore_index()

    def __del__(self):
        with open('out/index.pkl', 'wb') as output:
            pickle.dump(self.index, output, pickle.HIGHEST_PROTOCOL)

    def restore_index(self):
        with open('out/index.pkl', 'rb') as input:
            self.index = pickle.load(input)

    def search(self, query: str, number_of_results: int):
        if len(query.split(' ')) > 1:
            raise AttributeError('Only single word query\'s are supported for now')
        processed_query = self.get_tokens(query)
        results = list()
        for token in processed_query:
            pointers = self.index.get(token)
            if not pointers:
                continue
            i = 0
            for pointer in pointers:

                comment = CsvHelper.read_comment(pointer)
                results.append(comment)
                if i > number_of_results:
                    break
                i += 1

        return results

    def build_index(self, comments):
        for comment in comments:  # type: Comment
            for token in self.get_tokens(comment.comment_text):
                entry = self.index.get(token)  # type: list
                if not entry:
                    entry = list()
                entry.append(comment.pointer)
                self.index[token] = entry

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
