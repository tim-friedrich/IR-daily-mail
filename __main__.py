import os
import sys
import time

from scrapy.crawler import CrawlerProcess

from constants import OUT_DIR, COMMENTS, ARTICLES, SEARCH, INDEX
from helper.csv_helper import CsvHelper
from helper.model_helper import CommentsHelper, ArticlesHelper
from index import CommentsIndex
from models.comment import Comment
from spiders.article_spider import UpdateArticleSpider, InitialArticleSpider
from spiders.comment_spider import CommentSpider


def start_crawling(crawl_comments: bool):
    comments_helper = CommentsHelper()
    articles_helper = ArticlesHelper()

    # delete files if there has been an run on the same day before
    if os.path.isfile(OUT_DIR + comments_helper.get_csv_file_name()) and crawl_comments:
        os.remove(OUT_DIR + comments_helper.get_csv_file_name())

    if os.path.isfile(OUT_DIR + articles_helper.get_csv_file_name()) and not crawl_comments:
        os.remove(OUT_DIR + articles_helper.get_csv_file_name())

    be_polite = os.getenv('POLITE', False) == 'True'

    crawl_settings = {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_LEVEL': 'ERROR',
    }
    if be_polite:
        crawl_settings['DOWNLOAD_DELAY'] = 1

    print('Settings: {}'.format(crawl_settings))
    process = CrawlerProcess(crawl_settings)

    if crawl_comments:
        crawler_class = CommentSpider
        pass
    else:
        if articles_helper.get_latest_file():
            articles_helper.copy_last_article_file()
            crawler_class = UpdateArticleSpider
        else:
            crawler_class = InitialArticleSpider

    print('Crawler: ' + crawler_class.__name__)
    process.crawl(crawler_class)
    print('Start crawling. Please wait...')
    process.start()  # the script will block here until the crawling is finished

def start_indexing():
    print('Generating comments index...')
    comments = CsvHelper.read_object_list(CommentsHelper().get_latest_file(), Comment)
    index = CommentsIndex()
    index.build_index(comments)

    print('Index created')

def start_search(query: str):
    index = CommentsIndex()
    if query:
        print('Searching... (query: {})'.format(query))
        start_time = time.time()
        results = index.search(query, 6)
        print("--- %s seconds ---" % ((time.time() - start_time)))

        for comment in results:
            print(comment.comment_text)


available_arguments = [COMMENTS, ARTICLES, SEARCH, INDEX]

if not sys.argv or len(sys.argv) == 1 or not (sys.argv[1] in available_arguments):
    raise AttributeError('Please provide a parameter (e.g.: {})'.format(', '.join(available_arguments)))

if sys.argv[1] == COMMENTS:
    start_crawling(True)
elif sys.argv[1] == ARTICLES:
    start_crawling(False)
elif sys.argv[1] == INDEX:
    start_indexing()
elif sys.argv[1] == SEARCH:
    query = ''
    if len(sys.argv) == 3:
        query = sys.argv[2]
    start_search(query)
