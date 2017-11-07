from datetime import date

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from constants import ARTICLES_FILE_NAME_TEMPLATE
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
                           restrict_xpaths='//div[contains(@class, "debate column-split")]')),
        # find articles
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="archive-articles debate link-box"]'),
             callback='parse_article')
    )

    def parse_article(self, response):
        if response.status is not 200:
            print('Response Code was {}'.format(response.status))
            return
        url = response.url

        raw_date = response.xpath('//span[@class="article-timestamp article-timestamp-published"]/text()')
        article_date = raw_date.extract()[1].strip() if raw_date else ''

        comments_count = response.xpath('//span[@class="readerCommentsCount"]/text()').extract_first()

        article = Article(url, article_date, comments_count)
        print('Found article: {}'.format(article.article_url))
        CsvHelper.write_object_list(Article.get_csv_file_name(), [article])
