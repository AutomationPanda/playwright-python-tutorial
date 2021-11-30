"""
These tests cover DuckDuckGo searches.
"""


def test_basic_duckduckgo_search(page):

    # Given the DuckDuckGo home page is displayed
    page.goto('https://www.duckduckgo.com')

    # When the user searches for a phrase
    page.fill('#search_form_input_homepage', 'panda')
    page.click('#search_button_homepage')

    # Then the search result query is the phrase
    assert 'panda' == page.input_value('#search_form_input')

    # And the search result links pertain to the phrase
    page.locator('.result__title a.result__a >> nth=4').wait_for()
    titles = page.locator('.result__title a.result__a').all_text_contents()
    matches = [t for t in titles if 'panda' in t.lower()]
    assert len(matches) > 0

    # And the search result title contains the phrase
    assert 'panda' in page.title()
