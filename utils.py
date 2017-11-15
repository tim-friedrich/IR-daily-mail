import re
from datetime import timedelta, datetime

from constants import OUT_DIR


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def extract_date(string, pre_string):
    regex = '(?<=' + pre_string + ')\w*'
    regex_result = re.search(regex, string)
    if regex_result:
        return datetime.strptime(regex_result.group(), '%Y%m%d')
    return None


def check_file_name(file_name):
    if not file_name.startswith(OUT_DIR):
        file_name = OUT_DIR + file_name
    return file_name
