from playwright.sync_api import Page
import tldextract
from pathlib import Path
import csv
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class DynamicPageInfiniteScroll:

    @staticmethod
    def scroll(page: Page):
        prev_height = page.evaluate("() => document.body.scrollHeight")
        while True:
            page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1000)
            curr_height = page.evaluate("() => document.body.scrollHeight")
            if curr_height == prev_height:
                break
            prev_height = curr_height


class URLParser:
    @staticmethod
    def extract_domain(url: str) -> str:
        return tldextract.extract(url).domain


def save_data_to_file(data):
    output_path = BASE_DIR / "output"
    output_path.mkdir(exist_ok=True)
    scrapped_data = output_path / "scraped_data.csv"
    need_header = not (
        os.path.exists(scrapped_data) and os.path.getsize(scrapped_data) > 0
    )
    file_header = (
        "title",
        "additional_info",
        "description",
        "specs",
        "price",
        "domain",
        "url",
        "image_url",
    )

    with open(scrapped_data, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=file_header)
        if need_header:
            writer.writeheader()
        data = filter(lambda x: isinstance(x, dict), data)
        writer.writerows(data)
