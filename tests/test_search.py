"""
These tests cover DuckDuckGo searches.
"""

from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage


def test_basic_duckduckgo_search(page):
    search_page = DuckDuckGoSearchPage(page)
    result_page = DuckDuckGoResultPage(page)

    # Given the DuckDuckGo home page is displayed
    search_page.load()

    # When the user searches for a phrase
    search_page.search('panda')

    # Then the search result query is the phrase
    assert 'panda' == result_page.search_input_value()

    # And the search result links pertain to the phrase
    assert result_page.result_link_titles_contain_phrase('panda')

    # And the search result title contains the phrase
    assert 'panda' in result_page.title()
