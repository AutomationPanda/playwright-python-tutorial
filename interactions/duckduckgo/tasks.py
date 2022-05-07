"""
This module contains DuckDuckGo Tasks.
"""

from interactions.duckduckgo.pages import ResultPage, SearchPage
from interactions.duckduckgo.questions import result_link_titles
from playwright.sync_api import Page, expect
from screenplay.pattern import Actor, Task


class load_duckduckgo(Task):

    def perform_as(self, actor: Actor) -> None:
        page: Page = actor.using('page')
        page.goto(SearchPage.URL)


class search_duckduckgo_for(Task):

    def __init__(self, phrase: str) -> None:
        super().__init__()
        self.phrase = phrase
    
    def perform_as(self, actor: Actor) -> None:
        page: Page = actor.using('page')
        search_page = SearchPage(page)
        search_page.search_input.fill(self.phrase)
        search_page.search_button.click()


class verify_page_title_is(Task):

    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title
    
    def perform_as(self, actor: Actor) -> None:
        page: Page = actor.using('page')
        expect(page).to_have_title(self.title)


class verify_result_link_titles_contain(Task):

    def __init__(self, phrase: str, minimum: int = 1) -> None:
        super().__init__()
        self.phrase = phrase
        self.minimum = minimum
    
    def perform_as(self, actor: Actor) -> None:
        titles = actor.asks_for(result_link_titles())
        matches = [t for t in titles if self.phrase.lower() in t.lower()]
        assert len(matches) >= self.minimum


class verify_search_result_query_is(Task):

    def __init__(self, phrase: str) -> None:
        super().__init__()
        self.phrase = phrase

    def perform_as(self, actor: Actor) -> None:
        page: Page = actor.using('page')
        result_page = ResultPage(page)
        expect(result_page.search_input).to_have_value(self.phrase)
