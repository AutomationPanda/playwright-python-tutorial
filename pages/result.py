"""
This module contains DuckDuckGoResultPage,
the page object for the DuckDuckGo result page.
"""

from playwright.sync_api import Page
from typing import List


class DuckDuckGoResultPage:

    def __init__(self, page: Page) -> None:
        self.page = page
        self.result_links = page.locator('a[data-testid="result-title-a"]')
        self.search_input = page.locator('#search_form_input')
    
    def result_link_titles(self) -> List[str]:
        self.result_links.nth(4).wait_for()
        return self.result_links.all_text_contents()
    
    def result_link_titles_contain_phrase(self, phrase: str, minimum: int = 1) -> bool:
        titles = self.result_link_titles()
        matches = [t for t in titles if phrase.lower() in t.lower()]
        return len(matches) >= minimum
