from src.crawler import Spider


def main():
    url = input("Enter the Url: ")
    spider = Spider(url)
    spider.crawl()


if __name__ == "__main__":
    main()
