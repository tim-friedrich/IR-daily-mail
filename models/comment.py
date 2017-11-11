from datetime import date

from constants import COMMENTS_FILE_NAME_TEMPLATE


class Comment:
    def __init__(self, raw_comment, parent_comment_id=''):
        self.comment_id = raw_comment.get('id')
        self.article_url = 'http://www.dailymail.co.uk{}'.format(raw_comment.get('assetUrl'))
        self.comment_author = raw_comment.get('userAlias')
        self.comment_text = raw_comment.get('message')
        self.timestamp = raw_comment.get('dateCreated')
        self.parent_comment_id = parent_comment_id
        self.vote_count = raw_comment.get('voteCount')
        self.vote_rating = raw_comment.get('voteRating')

    @property
    def up_votes(self):
        return int((self.vote_count + self.vote_rating) / 2)

    @property
    def down_votes(self):
        return int((self.vote_count - self.vote_rating) / 2)

    @staticmethod
    def get_csv_file_name():
        return COMMENTS_FILE_NAME_TEMPLATE.format(date.today().strftime('%Y%m%d'))
