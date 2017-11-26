from models.csv_model import CsvItem
from utils import replace_disallowed_characters


class Comment(CsvItem):
    def __init__(self, raw_comment=None, parent_comment_id=None):
        if raw_comment:
            self.comment_id = raw_comment.get('id')
            self.article_url = 'http://www.dailymail.co.uk{}'.format(raw_comment.get('assetUrl'))
            self.comment_author = replace_disallowed_characters(raw_comment.get('userAlias'))
            self.comment_text = replace_disallowed_characters(raw_comment.get('message'))
            self.timestamp = raw_comment.get('dateCreated')
            self.parent_comment_id = parent_comment_id if parent_comment_id else ''
            self.vote_count = raw_comment.get('voteCount')
            self.vote_rating = raw_comment.get('voteRating')

    def __str__(self):
        return '{}: {}'.format(self.comment_author, self.comment_text)

    def __eq__(self, other):
        return self.comment_id == other.comment_id

    def __hash__(self):
        return hash(self.comment_id)

    @property
    def up_votes(self):
        return int((self.vote_count + self.vote_rating) / 2)

    @property
    def down_votes(self):
        return int((self.vote_count - self.vote_rating) / 2)

    @staticmethod
    def get_members():
        return ['comment_id',
                'article_url',
                'comment_author',
                'comment_text',
                'timestamp',
                'parent_comment_id',
                'vote_count',
                'vote_rating', ]
