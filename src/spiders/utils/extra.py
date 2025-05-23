from playwright.sync_api import Page
import tldextract


class DynamicPageInfiniteScroll:

    @staticmethod
    def scroll(page: Page):

        prev_height = None
        while True:
            curr_height = page.evaluate(
                "window.scrollTo(0, document.body.scrollHeight)"
            )
            page.wait_for_timeout(1000)
            if curr_height == prev_height:
                break
            prev_height = curr_height


class URLParser:
    @staticmethod
    def extract_domain(url: str) -> str:
        return tldextract.extract(url).domain
