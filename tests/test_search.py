"""
These tests cover DuckDuckGo searches.
"""

from pages.search import DuckDuckGoSearchPage


def test_basic_duckduckgo_search(page):
    search_page = DuckDuckGoSearchPage(page)

    # Given the DuckDuckGo home page is displayed
    search_page.load()

    # When the user searches for a phrase
    search_page.search('panda')

    # Then the search result query is the phrase
    assert 'panda' == page.input_value('#search_form_input')

    # And the search result links pertain to the phrase
    page.locator('.result__title a.result__a >> nth=4').wait_for()
    titles = page.locator('.result__title a.result__a').all_text_contents()
    matches = [t for t in titles if 'panda' in t.lower()]
    assert len(matches) > 0

    # And the search result title contains the phrase
    assert 'panda' in page.title()
