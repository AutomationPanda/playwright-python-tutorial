"""
These tests cover API tests for GitHub projects.
"""

import os
import pytest
import time

from playwright.sync_api import expect


def _get_env_var(varname):
    value = os.getenv(varname)
    assert value, f'{varname} is not set'
    return value


@pytest.fixture(scope='session')
def gh_username():
    return _get_env_var('GITHUB_USERNAME')


@pytest.fixture(scope='session')
def gh_password():
    return _get_env_var('GITHUB_PASSWORD')


@pytest.fixture(scope='session')
def gh_access_token():
    return _get_env_var('GITHUB_ACCESS_TOKEN')


@pytest.fixture(scope='session')
def gh_project_name():
    return _get_env_var('GITHUB_PROJECT_NAME')


@pytest.fixture(scope="session")
def gh_request_context(playwright, gh_access_token):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {gh_access_token}"}

    request_context = playwright.request.new_context(
        base_url="https://api.github.com",
        extra_http_headers=headers)

    yield request_context
    request_context.dispose()


@pytest.fixture()
def gh_project(gh_request_context, gh_username, gh_project_name):
    resource = f'/users/{gh_username}/projects'
    response = gh_request_context.get(resource)
    assert response.ok
    
    name_match = lambda x: x['name'] == gh_project_name
    filtered = filter(name_match, response.json())
    project = list(filtered)[0]
    assert project

    return project


@pytest.fixture()
def project_columns(gh_request_context, gh_project):
    response = gh_request_context.get(gh_project['columns_url'])
    assert response.ok

    columns = response.json()
    assert len(columns) >= 2
    return columns


@pytest.fixture()
def project_column_ids(project_columns):
    return list(map(lambda x: x['id'], project_columns))


def test_create_project_card(gh_request_context, project_column_ids):
    now = time.time()
    note = f'A new task at {now}!'

    c_response = gh_request_context.post(
        f'/projects/columns/{project_column_ids[0]}/cards',
        data={'note': note})
    assert c_response.ok

    card_id = c_response.json()['id']
    r_response = gh_request_context.get(f'/projects/columns/cards/{card_id}')
    assert r_response.ok
    assert r_response.json()['note'] == note


def test_move_project_card(gh_request_context, gh_project, project_column_ids, page, gh_username, gh_password):
    # Prep a card via API
    now = time.time()
    note = f'Move this card at {now}'
    c_response = gh_request_context.post(
        f'/projects/columns/{project_column_ids[0]}/cards',
        data={'note': note})
    assert c_response.ok

    # Login
    page.goto(f'https://github.com/login')
    page.fill('id=login_field', gh_username)
    page.fill('id=password', gh_password)
    page.click('input[name="commit"]')

    # Load the project page
    number = gh_project['number']
    page.goto(f'https://github.com/users/{gh_username}/projects/{number}')

    # Move a card via web UI
    page.drag_and_drop(f'text="{note}"', f'id=column-cards-{project_column_ids[1]}')

    # Verify the card is in the new column
    expect(page.locator(f'//div[@id="column-cards-{project_column_ids[1]}"]//p[contains(text(), "{note}")]')).to_be_visible()

    # Verify the backend is updated
    r_response = gh_request_context.get(f'/projects/columns/cards/{c_response.json()["id"]}')
    assert r_response.ok
    assert r_response.json()['column_url'].endswith(str(project_column_ids[1]))
