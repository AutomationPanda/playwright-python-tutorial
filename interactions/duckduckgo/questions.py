"""
This module contains DuckDuckGo Questions.
"""

from abc import ABC, abstractmethod
from interactions.duckduckgo.pages import ResultPage
from playwright.sync_api import Page
from screenplay.pattern import Actor, Question, Answer


# ------------------------------------------------------------
# DuckDuckGo Question parent class
# ------------------------------------------------------------

class DuckDuckGoQuestion(Question[Answer], ABC):

    @abstractmethod
    def request_on_page(self, actor: Actor, page: Page) -> Answer:
        pass

    def request_as(self, actor: Actor) -> Answer:
        page: Page = actor.using('page')
        return self.request_on_page(actor, page)
        

# ------------------------------------------------------------
# DuckDuckGo Questions
# ------------------------------------------------------------

class result_link_titles(DuckDuckGoQuestion[list[str]]):

    def request_on_page(self, _, page: Page) -> list[str]:
        result_page = ResultPage(page)
        result_page.result_links.nth(4).wait_for()
        return result_page.result_links.all_text_contents()
