"""
These tests cover API interactions for GitHub projects.
"""

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------

import time

from playwright.sync_api import APIRequestContext, Page, expect


# ------------------------------------------------------------
# A pure API test
# ------------------------------------------------------------

def test_create_project_card(
    gh_context: APIRequestContext,
    project_column_ids: list[str]) -> None:

    # Prep test data
    now = time.time()
    note = f'A new task at {now}'

    # Create a new card
    c_response = gh_context.post(
        f'/projects/columns/{project_column_ids[0]}/cards',
        data={'note': note})
    expect(c_response).to_be_ok()
    assert c_response.json()['note'] == note

    # Retrieve the newly created card
    card_id = c_response.json()['id']
    r_response = gh_context.get(f'/projects/columns/cards/{card_id}')
    expect(r_response).to_be_ok()
    assert r_response.json() == c_response.json()


# ------------------------------------------------------------
# A hybrid UI/API test
# ------------------------------------------------------------

def test_move_project_card(
    gh_context: APIRequestContext,
    gh_project: dict,
    project_column_ids: list[str],
    page: Page,
    gh_username: str,
    gh_password: str) -> None:

    # Prep test data
    source_col = project_column_ids[0]
    dest_col = project_column_ids[1]
    now = time.time()
    note = f'Move this card at {now}'

    # Create a new card via API
    c_response = gh_context.post(
        f'/projects/columns/{source_col}/cards',
        data={'note': note})
    expect(c_response).to_be_ok()

    # Log in via UI
    page.goto(f'https://github.com/login')
    page.locator('id=login_field').fill(gh_username)
    page.locator('id=password').fill(gh_password)
    page.locator('input[name="commit"]').click()

    # Load the project page
    page.goto(f'https://github.com/users/{gh_username}/projects/{gh_project["number"]}')

    # Verify the card appears in the first column
    card_xpath = f'//div[@id="column-cards-{source_col}"]//p[contains(text(), "{note}")]'
    expect(page.locator(card_xpath)).to_be_visible()

    # Move a card to the second column via web UI
    page.drag_and_drop(f'text="{note}"', f'id=column-cards-{dest_col}')

    # Verify the card is in the second column via UI
    card_xpath = f'//div[@id="column-cards-{dest_col}"]//p[contains(text(), "{note}")]'
    expect(page.locator(card_xpath)).to_be_visible()

    # Verify the backend is updated via API
    card_id = c_response.json()['id']
    r_response = gh_context.get(f'/projects/columns/cards/{card_id}')
    expect(r_response).to_be_ok()
    assert r_response.json()['column_url'].endswith(str(dest_col))
