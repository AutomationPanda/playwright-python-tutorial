"""
These tests cover API interactions for GitHub projects.
"""

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------

import time

from playwright.sync_api import expect


# ------------------------------------------------------------
# A pure API test
# ------------------------------------------------------------

def test_create_project_card(gh_context, project_column_ids):

    # Prep test data
    now = time.time()
    note = f'A new task at {now}'

    # Create a new card
    c_response = gh_context.post(
        f'/projects/columns/{project_column_ids[0]}/cards',
        data={'note': note})
    assert c_response.ok
    assert c_response.json()['note'] == note

    # Retrieve the newly created card
    card_id = c_response.json()['id']
    r_response = gh_context.get(f'/projects/columns/cards/{card_id}')
    assert r_response.ok
    assert r_response.json() == c_response.json()


# ------------------------------------------------------------
# A hybrid UI/API test
# ------------------------------------------------------------

def test_move_project_card(gh_context, gh_project, project_column_ids, page, gh_username, gh_password):

    # Prep test data
    col0 = project_column_ids[0]
    col1 = project_column_ids[1]
    now = time.time()
    note = f'Move this card at {now}'

    # Create a new card via API
    c_response = gh_context.post(
        f'/projects/columns/{col0}/cards',
        data={'note': note})
    assert c_response.ok

    # Log in via UI
    page.goto(f'https://github.com/login')
    page.fill('id=login_field', gh_username)
    page.fill('id=password', gh_password)
    page.click('input[name="commit"]')

    # Load the project page
    page.goto(f'https://github.com/users/{gh_username}/projects/{gh_project["number"]}')

    # Verify the card appears in the first column
    card_xpath = f'//div[@id="column-cards-{col0}"]//p[contains(text(), "{note}")]'
    expect(page.locator(card_xpath)).to_be_visible()

    # Move a card to the second column via web UI
    page.drag_and_drop(f'text="{note}"', f'id=column-cards-{col1}')

    # Verify the card is in the second column via UI
    card_xpath = f'//div[@id="column-cards-{col1}"]//p[contains(text(), "{note}")]'
    expect(page.locator(card_xpath)).to_be_visible()

    # Verify the backend is updated via API
    card_id = c_response.json()['id']
    r_response = gh_context.get(f'/projects/columns/cards/{card_id}')
    assert r_response.ok
    assert r_response.json()['column_url'].endswith(str(col1))
