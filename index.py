from models.comment import Comment


def build_index(comments):
    index = dict()
    for comment in comments:  # type: Comment
        for token in get_tokens(comment.comment_text):
            if token not in index:
                index[token] = comment.comment_id

    return index


def get_tokens(comment):
    return set(comment.split(' '))
