import os

import sys
from scrapy.crawler import CrawlerProcess

from constants import OUT_DIR
from models.article import Article
from models.comment import Comment
from spiders.article_spider import UpdateArticleSpider, InitialArticleSpider
from spiders.comment_spider import CommentSpider

if not sys.argv or len(sys.argv) == 1 or not (sys.argv[1] != 'articles' or sys.argv[1] != 'comments'):
    raise AttributeError('Please add "articles" or "comments" as arguments (Arguments: {})'.format(sys.argv))

crawl_comments = sys.argv[1] == 'comments'

# delete files if there has been an run on the same day before
if os.path.isfile(OUT_DIR + Comment.get_csv_file_name()) and crawl_comments:
    os.remove(OUT_DIR + Comment.get_csv_file_name())

if os.path.isfile(OUT_DIR + Article.get_csv_file_name()) and not crawl_comments:
    os.remove(OUT_DIR + Article.get_csv_file_name())

be_polite = os.getenv('POLITE', False) == 'True'

settings = {
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'LOG_LEVEL': 'ERROR',
}
if be_polite:
    settings['DOWNLOAD_DELAY'] = 1

print('Settings: {}'.format(settings))
process = CrawlerProcess(settings)

if crawl_comments:
    crawler_class = CommentSpider
    pass
else:
    if Article.get_latest_file():
        Article.copy_last_article_file()
        crawler_class = UpdateArticleSpider
    else:
        crawler_class = InitialArticleSpider

print('Crawler: ' + crawler_class.__name__)
process.crawl(crawler_class)
print('Start crawling. Please wait...')
process.start()  # the script will block here until the crawling is finished
