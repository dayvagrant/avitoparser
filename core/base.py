from splinter import Browser

ff_driver = "geckodriver"

import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    + "AppleWebKit/537.36 (KHTML, like Gecko) "
    + "Chrome/81.0.4044.138 Safari/537.36",
    "accept": "*/*",
}


class BrowserInit:
    """Init splinter brouser object with geckodriver."""

    def __init__(self, geckodriver_path: str = ff_driver):
        executable_path = {"executable_path": geckodriver_path}
        self.browser = Browser("firefox", headless=True, **executable_path)

    @classmethod
    def get_content(self, html):
        """Extract soup type."""
        soup = BeautifulSoup(html, "lxml")
        return soup

    @classmethod
    def get_html(url, headers=None, params=None):
        """Extract  get requests data."""
        r = requests.get(url, headers=HEADERS, params=params)
        r.encoding = "utf-8"
        return r
