from models.csv_model import CsvItem


class Article(CsvItem):
    def __init__(self, article_id=None, article_date=None):
        if article_id and article_date:
            self.article_id = article_id
            self.date = article_date

    @staticmethod
    def get_members():
        return [
            'article_id',
            'date'
        ]
