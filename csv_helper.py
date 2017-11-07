import csv


class CsvHelper:
    @staticmethod
    def write_comments(file_name, comments):
        comments = [comment.__dict__ for comment in comments]
        if not comments:
            return
        with open(file_name, newline='', mode='a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, comments[0].keys(), quoting=csv.QUOTE_ALL)
            writer.writeheader()

            for comment in comments:
                writer.writerow(comment)
