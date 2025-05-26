from playwright.sync_api import sync_playwright
from typing import Optional
from src.spiders.utils.extra import (
    DynamicPageInfiniteScroll,
    URLParser,
    save_data_to_file,
)
import curl_cffi
import asyncio
from parsel import Selector


class DynamicPageSpider(DynamicPageInfiniteScroll):
    def __init__(self, url: str):
        self.url = url

    def fetch(self) -> Optional[str]:
        pass

    def parse_data(content: str):
        pass


class _StaticPageSpider(URLParser):
    def __init__(self, url: str):
        self.url = url
        self.domain = self.extract_domain(self.url)

    def __fetch_all_urls(self):
        url = self.url
        product_urls = []

        while url:
            response = curl_cffi.get(url, impersonate="chrome")
            content = response.text
            product_urls.extend(self.parse_products_urls(content))
            url = self.next_page(content)

        return product_urls

    def parse_products_urls(self, content: str):
        raise NotImplementedError("Subclasses must implement parse_products_urls")

    def next_page(self, content: str):
        raise NotImplementedError("Subclasses must implement next_page")

    def parse_data(self, content: str):
        raise NotImplementedError("Subclasses must implement parse_data")

    async def __fetch_and_parse(self, url, session: curl_cffi.AsyncSession):
        response = await session.get(url, impersonate="chrome")
        content = response.text
        result = self.parse_details(content)
        result["domain"] = self.domain
        result["url"] = url
        return result

    async def __fetch_mutiple(self, urls: list[str]):
        async with curl_cffi.AsyncSession(max_clients=10, timeout=15) as session:
            tasks = [self.__fetch_and_parse(u, session) for u in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results

    def crawl(self):
        product_urls = self.__fetch_all_urls()
        parsed_data = asyncio.run(self.__fetch_mutiple(product_urls))
        save_data_to_file(parsed_data)


class AlfatahSpider(_StaticPageSpider):
    def parse_products_urls(self, content: str):
        selector = Selector(text=content)
        return selector.css(
            "div.products a.woocommerce-LoopProduct-link::attr(href)"
        ).getall()

    def next_page(self, content: str):
        selector = Selector(text=content)
        return selector.css("ul.page-numbers .next::attr(href)").get()

    def parse_details(self, content):
        selector = Selector(text=content)
        title = selector.css("h1.product_title::text").get()
        price = selector.css("div.summary p.price bdi::text").get()
        img_url = selector.css("span.nickx-popup::attr(href)").extract_first()
        description = list()
        for li in selector.css("#tab-description ul li"):
            description.append("".join(map(str.strip, li.css("::text").getall())))
        if not description:
            description.append(selector.css("#tab-description p::text").get())
        additional_info = list()
        for tr in selector.css("#tab-additional_information table tr"):
            additional_info.append(" ".join(map(str.strip, tr.css("::text").getall())))
        return {
            "title": title,
            "additional_info": "\n".join(additional_info),
            "description": "\n".join(description),
            "price": price,
            "image_url": img_url,
        }
