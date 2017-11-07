import os

from scrapy.crawler import CrawlerProcess

from constants import OUT_DIR
from models.article import Article
from models.comment import Comment
from spiders.article_spider import ArticleSpider

if os.path.isfile(OUT_DIR + Comment.get_csv_file_name()):
    os.remove(OUT_DIR + Comment.get_csv_file_name())

if os.path.isfile(OUT_DIR + Article.get_csv_file_name()):
    os.remove(OUT_DIR + Article.get_csv_file_name())


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'LOG_LEVEL': 'ERROR'
})

process.crawl(ArticleSpider)
process.start()  # the script will block here until the crawling is finished
