import time

from loguru import logger
from tqdm import tqdm

from core.base import BrowserInit
from core.extracters import extract_data_from_page
from core.utils import format_url_for_search


class AvitoParser(BrowserInit):
    def __init__(self, url: str):
        super().__init__()
        self.url = format_url_for_search(url)
        self.visit_page(self.url)
        self.preload_data = self.get_content(self.browser.html)
        self.count_items_of_sales = self.count_items_of_sales(self.preload_data)
        self.start_page = 1
        self.max_page = self.all_pagination(self.preload_data)

    def visit_page(self, url):
        self.browser.visit(url)

    def get_url(self):
        return self.browser.url

    def all_pagination(self, soup):
        try:
            item = soup.find_all("span", class_="pagination-item-JJq_j")
            pages = item[-2]
            pages = pages.get_text(strip=True)
            pages = int(pages)
            return pages
        except IndexError:
            return 0

    def count_items_of_sales(self, soup):
        item = soup.find("span", attrs={"data-marker": "page-title/count"}).get_text()
        return int(item)

    def get_sales_items(self, with_recomendations: bool = True, debug=False):
        items_for_sold = list()
        try:
            if self.start_page == 1:
                extract_data_from_page(
                    self.preload_data, items_for_sold, with_recomendations, debug
                )
            if self.max_page > 0:
                for i in tqdm(range(2, self.max_page + 1)):
                    self.start_page = i
                    self.visit_page(self.url + f"&p={self.start_page}")
                    time.sleep(3)
                    extract_data_from_page(
                        self.get_content(self.browser.html),
                        items_for_sold,
                        with_recomendations,
                        debug,
                    )
            return items_for_sold
        except Exception as ex:
            logger.error(ex)
