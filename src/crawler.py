from src.spiders.spiders import AlfatahSpider, PhilipsSpider
from src.spiders.utils.extra import URLParser


class Spider(URLParser):
    def __init__(self, url):
        self.SPIDERS = {"alfatah": AlfatahSpider, "philipsappliances": PhilipsSpider}
        self.url = url
        self.domain = self.extract_domain(url)

    def crawl(self):
        if spider := self.SPIDERS.get(self.domain):
            curr_spider = spider(self.url)
            curr_spider.crawl()
        else:
            raise ModuleNotFoundError(f"{self.domain} is not Implemented")
