import re
from datetime import timedelta, datetime


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def extract_date(string, pre_string):
    regex = '(?<=' + pre_string + ')\w*'
    regex_result = re.search(regex, string)
    if regex_result:
        return datetime.strptime(regex_result.group(), '%Y%m%d')
    return None

