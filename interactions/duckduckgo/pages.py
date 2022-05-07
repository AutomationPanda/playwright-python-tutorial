"""
This module contains DuckDuckGo pages.
"""

from playwright.sync_api import Page


class SearchPage:

    URL = 'https://www.duckduckgo.com'

    def __init__(self, page: Page) -> None:
        self.page = page
        self.search_button = page.locator('#search_button_homepage')
        self.search_input = page.locator('#search_form_input_homepage')


class ResultPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.result_links = page.locator('a[data-testid="result-title-a"]')
        self.search_input = page.locator('#search_form_input')
    