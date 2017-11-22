import logging
import os
import sys
import time

from scrapy.crawler import CrawlerProcess

from constants import COMMENTS, ARTICLES, SEARCH, INDEX
from helper.csv_helper import CsvHelper
from helper.model_helper import CommentsHelper, ArticlesHelper
from index import CommentsIndex
from models.comment import Comment
from spiders.article_spider import UpdateArticleSpider, InitialArticleSpider
from spiders.comment_spider import CommentSpider
from utils import delete_file_if_exists


def start_crawling(crawl_comments: bool):
    comments_helper = CommentsHelper()
    articles_helper = ArticlesHelper()

    # delete files if there has been an run on the same day before
    if crawl_comments:
        delete_file_if_exists(comments_helper.get_csv_file_name())
    else:
        delete_file_if_exists(articles_helper.get_csv_file_name())

    try:
        politeness_delay = float(os.getenv('POLITE', 0))
    except ValueError:
        logging.info('Failed to parse env variable POLITE (value: {})'.format(os.getenv('POLITE')))
        politeness_delay = None

    crawl_settings = {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_LEVEL': 'ERROR',
    }
    if politeness_delay:
        crawl_settings['DOWNLOAD_DELAY'] = politeness_delay

    logging.info('Settings: {}'.format(crawl_settings))

    process = CrawlerProcess(crawl_settings)

    if crawl_comments:
        if not articles_helper.get_latest_file():
            logging.error('No articles file. You need to crawl articles at least once before comments.')
            return
        crawler_class = CommentSpider

    else:
        if articles_helper.get_latest_file():
            articles_helper.copy_last_article_file()
            crawler_class = UpdateArticleSpider
        else:
            crawler_class = InitialArticleSpider

    logging.info('Crawler: ' + crawler_class.__name__)
    process.crawl(crawler_class)
    logging.info('Start crawling. Please wait...')
    logging.getLogger('scrapy').setLevel(logging.ERROR)

    process.start()  # the script will block here until the crawling is finished


def start_indexing():
    logging.info('Generating comments index...')

    comments = CsvHelper.read_object_list(CommentsHelper().get_latest_file(), Comment)
    index = CommentsIndex()
    index.build_index(comments)

    logging.info('Index created')


def start_search(query: str):
    index = CommentsIndex()
    if query:
        logging.info('Searching... (query: {})'.format(query))
        start_time = time.time()
        results = index.search(query, 6)
        logging.info("--- %s seconds ---" % ((time.time() - start_time)))

        for comment in results:
            print(comment.comment_text)


available_arguments = [COMMENTS, ARTICLES, SEARCH, INDEX]

FORMAT = '%(asctime)s %(name)-14s %(levelname)-8s %(message)s'

logging.basicConfig(format=FORMAT, level=logging.DEBUG)

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
