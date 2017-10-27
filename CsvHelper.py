import csv


class CsvHelper:

    @staticmethod
    def write_comments(file_name, comments):
        comments = [comment.__dict__ for comment in comments]
        with open('comments.csv', newline='', mode='w', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, comments[0].keys())
            writer.writeheader()

            for comment in comments:
                writer.writerow(comment)
