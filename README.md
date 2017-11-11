# IR-daily-mail

###Crawl articles
Run `__main__.py articles`
- crawles all articles until yesterday
- updates article loist if there is already an articles-\<Ymd>.csv

###Crawl comments (crawl articles before!)
Run `__main__.py comments`
- Iterates through articles-\<Ymd>.csv

### Misc
You can apply politeness by setting environment variable `POLITE=True`