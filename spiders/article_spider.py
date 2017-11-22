import re
import logging
from abc import ABC
from datetime import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from helper.csv_helper import CsvHelper
from helper.model_helper import ArticlesHelper
from models.article import Article
from utils import date_range, extract_date


class ArticleSpider(CrawlSpider, ABC):
    name = 'dailymail sitemap'
    start_urls = ['http://www.dailymail.co.uk/home/sitemaparchive/index.html']

    def __init__(self, *a, **kw):
        self.helper = ArticlesHelper()
        self.csv_helper = CsvHelper(self.helper.get_csv_file_name())
        self.counter = 0
        super().__init__(*a, **kw)

    def parse_article(self, response):
        if response.status is not 200:
            logging.error('Response Code was {}'.format(response.status))
            return

        urls = response.xpath('//ul[@class="archive-articles debate link-box"]//li//@href').extract()
        articles = []
        for url in urls:
            article_date = datetime.strptime(re.search('(?<=day_)\w*', response.url).group(), '%Y%m%d')
            articles.append(Article(url, article_date))

        if articles:
            self.csv_helper.write_object_list(articles)
            self.counter += len(articles)
            print('\rArticles crawled: ' + '{:,}'.format(self.counter), end='')

    @staticmethod
    def get_update_rules():
        allowed_dates = []

        latest_file = ArticlesHelper().get_latest_file()
        date_of_latest_file = extract_date(latest_file, 'articles-')
        if not date_of_latest_file:
            return allowed_dates

        for single_date in date_range(date_of_latest_file, datetime.today()):
            allowed_dates.append(single_date.strftime("%Y%m%d"))

        return (
            Rule(LinkExtractor(allow='sitemaparchive/month',
                               restrict_xpaths='//ul[@class="archive-index home link-box"]')),
            # find days except today to have a clear knowledge what has been crawled
            Rule(LinkExtractor(allow=allowed_dates,
                               restrict_xpaths='//div[contains(@class, "debate column-split")]'),
                 callback='parse_article'),
        )


class InitialArticleSpider(ArticleSpider):
    rules = (Rule(LinkExtractor(allow='sitemaparchive/month',
                                restrict_xpaths='//ul[@class="archive-index home link-box"]')),
             # find days except today to have a clear knowledge what has been crawled
             Rule(LinkExtractor(allow='sitemaparchive/day', deny=datetime.today().strftime('%Y%m%d'),
                                restrict_xpaths='//div[contains(@class, "debate column-split")]'),
                  callback='parse_article'),
             )


class UpdateArticleSpider(ArticleSpider):
    rules = ArticleSpider.get_update_rules()
