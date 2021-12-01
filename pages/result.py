"""
This module contains DuckDuckGoResultPage,
the page object for the DuckDuckGo result page.
"""

class DuckDuckGoResultPage:

    RESULT_LINKS = '.result__title a.result__a'
    SEARCH_INPUT = '#search_form_input'
    
    def __init__(self, page):
        self.page = page
    
    def result_link_titles(self):
        self.page.locator(f'{self.RESULT_LINKS} >> nth=4').wait_for()
        titles = self.page.locator(self.RESULT_LINKS).all_text_contents()
        return titles
    
    def result_link_titles_contain_phrase(self, phrase, minimum=1):
        titles = self.result_link_titles()
        matches = [t for t in titles if phrase.lower() in t.lower()]
        return len(matches) >= minimum

    def search_input_value(self):
        return self.page.input_value(self.SEARCH_INPUT)
    
    def title(self):
        return self.page.title()
