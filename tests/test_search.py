"""
These tests cover DuckDuckGo searches.
"""

import pytest

from interactions.duckduckgo.tasks import *
from screenplay.pattern import Actor


ANIMALS = [
    'panda',
    'python',
    'polar bear',
    'parrot',
    'porcupine',
    'parakeet',
    'pangolin',
    'panther',
    'platypus',
    'peacock'
]


@pytest.mark.parametrize('phrase', ANIMALS)
def test_basic_duckduckgo_search(phrase: str, actor: Actor) -> None:
    
    # Given the DuckDuckGo home page is displayed
    actor.attempts_to(load_duckduckgo())

    # When the user searches for a phrase
    actor.attempts_to(search_duckduckgo_for(phrase))

    # Then the search result query is the phrase
    actor.attempts_to(verify_search_result_query_is(phrase))

    # And the search result links pertain to the phrase
    actor.attempts_to(verify_result_link_titles_contain(phrase))

    # And the search result title contains the phrase
    actor.attempts_to(verify_page_title_is(f'{phrase} at DuckDuckGo'))
