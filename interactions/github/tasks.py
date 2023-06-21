"""
This module contains GitHub Project Tasks.
"""

from abc import ABC, abstractmethod
from playwright.sync_api import Page, expect
from screenplay.pattern import Actor, Task


# ------------------------------------------------------------
# GitHub Project Task parent class
# ------------------------------------------------------------

class GitHubProjectTask(Task, ABC):

    @abstractmethod
    def perform_on_page(self, actor: Actor, page: Page) -> None:
        pass

    def perform_as(self, actor: Actor) -> None:
        page: Page = actor.using('page')
        self.perform_on_page(actor, page)


# ------------------------------------------------------------
# GitHub Project Tasks
# ------------------------------------------------------------

class log_into_github_as(GitHubProjectTask):

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
    
    def perform_on_page(self, actor: Actor, page: Page) -> None:
        page.goto(f'https://github.com/login')
        page.locator('id=login_field').fill(self.username)
        page.locator('id=password').fill(self.password)
        page.locator('input[name="commit"]').click()


class load_github_project_for(GitHubProjectTask):

    def __init__(self, username: str, project_number: str) -> None:
        self.username = username
        self.project_number = project_number
    
    def perform_on_page(self, actor: Actor, page: Page) -> None:
        page.goto(f'https://github.com/users/{self.username}/projects/{self.project_number}')


class verify_card_appears_with(GitHubProjectTask):

    def __init__(self, column_id: str, note: str) -> None:
        self.column_id = column_id
        self.note = note
    
    def perform_on_page(self, actor: Actor, page: Page) -> None:
        card_xpath = f'//div[@id="column-cards-{self.column_id}"]//p[contains(text(), "{self.note}")]'
        expect(page.locator(card_xpath)).to_be_visible()
        

class move_card_to(GitHubProjectTask):

    def __init__(self, column_id: str, note: str) -> None:
        self.column_id = column_id
        self.note = note

    def perform_on_page(self, actor: Actor, page: Page) -> None:
        page.drag_and_drop(f'text="{self.note}"', f'id=column-cards-{self.column_id}')