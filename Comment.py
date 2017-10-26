class Comment:
    def __init__(self, raw_comment, parent_comment_id=''):
        self.comment_id = raw_comment.get('id')
        self.article_url = raw_comment.get('assetHeadline')
        self.comment_author = raw_comment.get('userAlias')
        self.comment_text = raw_comment.get('message').encode('utf-8')
        self.timestamp = raw_comment.get('dateCreated')
        self.parent_comment_id = parent_comment_id
