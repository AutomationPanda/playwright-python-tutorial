"""
These tests cover DuckDuckGo searches.
"""

from playwright.sync_api import expect, Page


def test_basic_duckduckgo_search(search_page, result_page) -> None:
    
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

