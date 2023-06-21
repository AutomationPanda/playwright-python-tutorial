"""
This module contains DuckDuckGo Tasks.
"""

from abc import ABC, abstractmethod
from interactions.duckduckgo.pages import ResultPage, SearchPage
from interactions.duckduckgo.questions import result_link_titles
from playwright.sync_api import Page, expect
from screenplay.pattern import Actor, Task


# ------------------------------------------------------------
# DuckDuckGo Task parent class
# ------------------------------------------------------------

class DuckDuckGoTask(Task, ABC):

    @abstractmethod
    def perform_on_page(self, actor: Actor, page: Page) -> None:
        pass

    def perform_as(self, actor: Actor) -> None:
        page: Page = actor.using('page')
        self.perform_on_page(actor, page)


# ------------------------------------------------------------
# DuckDuckGo Tasks
# ------------------------------------------------------------

class load_duckduckgo(DuckDuckGoTask):

    def perform_on_page(self, _, page: Page) -> None:
        page.goto(SearchPage.URL)


class search_duckduckgo_for(DuckDuckGoTask):

    def __init__(self, phrase: str) -> None:
        super().__init__()
        self.phrase = phrase
    
    def perform_on_page(self, _, page: Page) -> None:
        search_page = SearchPage(page)
        search_page.search_input.fill(self.phrase)
        search_page.search_button.click()


class verify_page_title_is(DuckDuckGoTask):

    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title
    
    def perform_on_page(self, _, page: Page) -> None:
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


class verify_search_result_query_is(DuckDuckGoTask):

    def __init__(self, phrase: str) -> None:
        super().__init__()
        self.phrase = phrase

    def perform_on_page(self, _, page: Page) -> None:
        result_page = ResultPage(page)
        expect(result_page.search_input).to_have_value(self.phrase)
