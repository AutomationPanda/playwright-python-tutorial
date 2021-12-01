"""
This module contains DuckDuckGoSearchPage,
the page object for the DuckDuckGo search page.
"""

class DuckDuckGoSearchPage:

    SEARCH_BUTTON = '#search_button_homepage'
    SEARCH_INPUT = '#search_form_input_homepage'

    URL = 'https://www.duckduckgo.com'

    def __init__(self, page):
        self.page = page
    
    def load(self):
        self.page.goto(self.URL)
    
    def search(self, phrase):
        self.page.fill(self.SEARCH_INPUT, phrase)
        self.page.click(self.SEARCH_BUTTON)
