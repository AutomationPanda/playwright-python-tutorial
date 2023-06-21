"""
These tests cover API interactions for GitHub projects.
"""

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------

import time

from interactions.github.calls import *
from interactions.github.tasks import *
from screenplay.pattern import Actor


# ------------------------------------------------------------
# A pure API test
# ------------------------------------------------------------

def test_create_project_card(
    gh_actor: Actor,
    project_column_ids: list[str]) -> None:

    # Prep test data
    now = time.time()
    note = f'A new task at {now}'

    # Create a new card
    c_response = gh_actor.calls(create_card(project_column_ids[0], note))

    # Retrieve the newly created card
    card_id = c_response.json()['id']
    r_response = gh_actor.calls(retrieve_card(card_id))
    assert r_response.json() == c_response.json()


# ------------------------------------------------------------
# A hybrid UI/API test
# ------------------------------------------------------------

def test_move_project_card(
    gh_actor: Actor,
    gh_project: dict,
    project_column_ids: list[str],
    gh_username: str,
    gh_password: str) -> None:

    # Prep test data
    source_col = project_column_ids[0]
    dest_col = project_column_ids[1]
    now = time.time()
    note = f'Move this card at {now}'

    # Create a new card via API
    c_response = gh_actor.calls(create_card(source_col, note))

    # Log in via UI
    gh_actor.attempts_to(log_into_github_as(gh_username, gh_password))

    # Load the project page
    gh_actor.attempts_to(load_github_project_for(gh_username, gh_project["number"]))

    # Verify the card appears in the first column
    gh_actor.attempts_to(verify_card_appears_with(source_col, note))

    # Move a card to the second column via web UI
    gh_actor.attempts_to(move_card_to(dest_col, note))

    # Verify the card is in the second column via UI
    gh_actor.attempts_to(verify_card_appears_with(dest_col, note))

    # Verify the backend is updated via API
    card_id = c_response.json()['id']
    r_response = gh_actor.calls(retrieve_card(card_id))
    assert r_response.json()['column_url'].endswith(str(dest_col))
