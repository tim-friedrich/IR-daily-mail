from copy import copy

from comments_index import CommentsIndex
from helper.csv_helper import CsvHelper
from models.comment import Comment


class CommentSearch:
    def __init__(self, index: CommentsIndex):
        self.index = index

    def boolean_search(self, query):
        if query.startswith('’') and query.endswith('’'):
            return self.phrase_query_search(query)
        processed_query = self.index.get_tokens(query)
        result_stack = []
        pending_operation = ''
        is_wildcard = False

        for i, token in enumerate(processed_query):
            if is_wildcard:
                is_wildcard = False
                i += 1
                continue
            if len(processed_query) > i + 1 and processed_query[i + 1] == '*':
                is_wildcard = True

            if token == 'and' or token == 'or' or token == 'not':
                pending_operation = token.upper()
            else:
                results = set()
                postings = self.index.get_postings(token, is_wildcard)
                if not postings:
                    continue
                for posting_pointer in postings:
                    comment = CsvHelper.read_comment(self.index.index.get_file(),
                                                     *posting_pointer.rstrip().split(';'))  # type: Comment
                    results.add(comment)
                result_stack.append(results)

                if pending_operation != '':
                    results = getattr(self, pending_operation)(result_stack.pop(), result_stack.pop())
                    result_stack.append(results)
        return result_stack[-1]

    def phrase_query_search(self, query):
        processed_query = self.index.get_tokens(query)
        processed_query = [token for token in processed_query if token != '’']

        latest_results = set()
        for i, token in enumerate(processed_query):
            current_results = set()
            postings = self.index.get_postings(token)
            if not postings:
                continue

            for posting_pointer in postings:
                comment = CsvHelper.read_comment(self.index.index.get_file(),
                                                 *posting_pointer.rstrip().split(';'))  # type: Comment

                if i == 0:
                    current_results.add(comment)
                else:
                    for item in latest_results:  # type: Comment
                        if comment.comment_id == item.comment_id:
                            if comment.token_position - 1 == item.token_position:
                                current_results.add(comment)
            latest_results = copy(current_results)
            i += 1
        return latest_results

    def AND(self, left_bag, right_bag):
        return left_bag.intersection(right_bag)

    def NOT(self, left_bag, right_bag):
        return right_bag - left_bag

    def OR(self, left_bag, right_bag):
        return left_bag.union(right_bag)
