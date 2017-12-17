import argparse
import logging
import os
import time

from scrapy.crawler import CrawlerProcess

from helper.index_file_helper import IndexFileHelper
from helper.model_helper import CommentsHelper, ArticlesHelper
from comments_index import CommentsIndex
from search import CommentSearch
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
    file_helper = IndexFileHelper()
    os.remove(file_helper.posting_file)
    os.remove(file_helper.index_file)
    os.remove('out/frequency')
    CommentsIndex(rebuild_index=True)

    logging.info('Index created')


def start_search(query: str):
    index = CommentsIndex()
    search = CommentSearch(index)
    if query:
        logging.info('Searching... (query: {})'.format(query).encode())
        start_time = time.time()
        results = search.vector_space_search(query)
        logging.info('--- %s seconds ---' % (time.time() - start_time))

        for comment in results:
            print(comment)

        logging.info('Number of results: {}'.format(len(results)))


def compress_index():
    IndexFileHelper().compress_index('out/posting_list')


FORMAT = '%(asctime)s %(name)-14s %(levelname)-8s %(message)s'
if not os.path.exists('logs'):
    os.mkdir('logs')
logging_file_name = 'logs/{}.log'.format(time.strftime("%Y%m%d-%H%M%S"))

logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename=logging_file_name)
logging.getLogger().addHandler(logging.StreamHandler())

parser = argparse.ArgumentParser(description='Comment Search for Daily Mail.')
parser.add_argument('--comments',
                    help='Crawl for comments, based on the crawled articles.',
                    dest='comments',
                    action='store_true')
parser.add_argument('--articles',
                    help='Crawl for articles.',
                    dest='articles',
                    action='store_true')
parser.add_argument('--index',
                    help='Generate index for crawled comments.',
                    dest='index',
                    action='store_true')
parser.add_argument('--search',
                    help='Search for the following query.',
                    dest='search',
                    action='store')
parser.add_argument('--compress',
                    help='Compress the index.',
                    dest='compress',
                    action='store_true')

args = parser.parse_args()

if args.comments:
    start_crawling(True)
elif args.articles:
    start_crawling(False)
elif args.index:
    start_indexing()
elif args.search:
    start_search(args.search)
elif args.compress:
    compress_index()
