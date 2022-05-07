"""
This module contains DuckDuckGo Questions.
"""

from interactions.duckduckgo.pages import ResultPage
from playwright.sync_api import Page
from screenplay.pattern import Actor, Question


class result_link_titles(Question[list[str]]):

    def request_as(self, actor: Actor) -> list[str]:
        page: Page = actor.using('page')
        result_page = ResultPage(page)
        result_page.result_links.nth(4).wait_for()
        return result_page.result_links.all_text_contents()
