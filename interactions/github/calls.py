"""
This module contains REST API calls for GitHub Projects.
"""

from abc import ABC, abstractmethod
from playwright.sync_api import APIRequestContext, APIResponse, expect
from screenplay.pattern import Actor, Question


# ------------------------------------------------------------
# GitHub Project Call parent class
# ------------------------------------------------------------

class GitHubProjectCall(Question[APIResponse], ABC):

    @abstractmethod
    def call_as(self, actor: Actor, context: APIRequestContext) -> APIResponse:
        pass

    def request_as(self, actor: Actor) -> APIResponse:
        context: APIRequestContext = actor.using('gh_context')
        return self.call_as(actor, context)


# ------------------------------------------------------------
# GitHub Project Calls
# ------------------------------------------------------------

class create_card(GitHubProjectCall):

    def __init__(self, column_id: str, note: str | None = None) -> None:
        self.column_id = column_id
        self.note = note
    
    def call_as(self, actor: Actor, context: APIRequestContext) -> APIResponse:
        response = context.post(
            f'/projects/columns/{self.column_id}/cards',
            data={'note': self.note})
        expect(response).to_be_ok()
        return response


class retrieve_card(GitHubProjectCall):

    def __init__(self, card_id: str) -> None:
        self.card_id = card_id
    
    def call_as(self, actor: Actor, context: APIRequestContext) -> APIResponse:
        response = context.get(f'/projects/columns/cards/{self.card_id}')
        expect(response).to_be_ok()
        return response