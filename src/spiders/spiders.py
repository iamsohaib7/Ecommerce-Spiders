from playwright.sync_api import sync_playwright
from typing import Optional
from src.spiders.utils.extra import DynamicPageInfiniteScroll
import curl_cffi
from parsel import Selector


class DynamicPageSpider(DynamicPageInfiniteScroll):
    def __init__(self, url: str):
        self.url = url

    def fetch(self) -> Optional[str]:
        pass

    def parse_data(content: str):
        pass


class _StaticPageSpider:
    def __init__(self, url: str):
        self.url = url

    def __fetch_all_urls(self):
        url = self.url
        product_urls = []

        while url:
            response = curl_cffi.get(url, impersonate="chrome")
            print(url)
            content = response.text
            product_urls.extend(self.__parse_products_urls(content))
            url = self.__next_page(content)

        return product_urls

    def parse_products_urls(self, content: str):
        raise NotImplementedError("Subclasses must implement parse_products_urls")

    def __next_page(self, content: str):
        raise NotImplementedError("Subclasses must implement next_page")

    def crawl(self):
        pass



class AlfatahSpider(_StaticPageSpider):
    def parse_products_urls(self, content: str):
        selector = Selector(text=content)
        return selector.css(
            "div.products a.woocommerce-LoopProduct-link::attr(href)"
        ).getall()

    def next_page(self, content: str):
        selector = Selector(text=content)
        return selector.css("ul.page-numbers .next::attr(href)").get()
