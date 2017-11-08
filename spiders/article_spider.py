import re
from datetime import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from csv_helper import CsvHelper
from models.article import Article


class ArticleSpider(CrawlSpider):
    name = 'dailymail sitemap'
    start_urls = ['http://www.dailymail.co.uk/home/sitemaparchive/index.html']
    rules = (
        # find months
        Rule(LinkExtractor(allow='sitemaparchive/month',
                           restrict_xpaths='//ul[@class="archive-index home link-box"]')),
        # find days
        Rule(LinkExtractor(allow='sitemaparchive/day',
                           restrict_xpaths='//div[contains(@class, "debate column-split")]'), callback='parse_article'),
    )

    def parse_article(self, response):
        if response.status is not 200:
            print('Response Code was {}'.format(response.status))
            return
        url = response.url

        urls = response.xpath('//ul[@class="archive-articles debate link-box"]//li//@href').extract()
        for url in urls:
            article_date = datetime.strptime(re.search('(?<=day_)\w*', response.url).group(), '%Y%m%d')
            article = Article(url, article_date)
            print('Date:{}, URL: {}'.format(article_date, article.article_url))
            CsvHelper.write_object_list(Article.get_csv_file_name(), [article])
