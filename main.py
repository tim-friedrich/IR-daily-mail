from scrapy.crawler import CrawlerProcess

from comment_spider import CommentSpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'LOG_LEVEL': 'ERROR'
})

process.crawl(CommentSpider)
process.start()  # the script will block here until the crawling is finished
