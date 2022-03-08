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
def github_username():
    return _get_env_var('GITHUB_USERNAME')


@pytest.fixture(scope='session')
def github_password():
    return _get_env_var('GITHUB_PASSWORD')


@pytest.fixture(scope='session')
def github_access_token():
    return _get_env_var('GITHUB_ACCESS_TOKEN')


@pytest.fixture(scope='session')
def github_project_name():
    return _get_env_var('GITHUB_PROJECT_NAME')


@pytest.fixture(scope='session')
def github_project_number():
    return _get_env_var('GITHUB_PROJECT_NUMBER')


@pytest.fixture(scope="session")
def github_request_context(playwright, github_username, github_access_token):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {github_access_token}"}

    request_context = playwright.request.new_context(
        base_url="https://api.github.com",
        extra_http_headers=headers)

    yield request_context
    request_context.dispose()


@pytest.fixture()
def github_project(github_request_context, github_username, github_project_name):
    resource = f'/users/{github_username}/projects'
    response = github_request_context.get(resource)
    assert response.ok
    
    name_match = lambda x: x['name'] == github_project_name
    filtered = filter(name_match, response.json())
    project = list(filtered)[0]
    assert project

    return project


@pytest.fixture()
def project_columns(github_request_context, github_project):
    response = github_request_context.get(github_project['columns_url'])
    assert response.ok

    columns = response.json()
    assert len(columns) >= 2
    return columns


@pytest.fixture()
def project_column_ids(project_columns):
    return list(map(lambda x: x['id'], project_columns))


def test_create_project_card(github_request_context, project_column_ids):
    now = time.time()
    note = f'A new task at {now}!'

    c_response = github_request_context.post(
        f'/projects/columns/{project_column_ids[0]}/cards',
        data={'note': note})
    assert c_response.ok

    card_id = c_response.json()['id']
    r_response = github_request_context.get(f'/projects/columns/cards/{card_id}')
    assert r_response.ok
    assert r_response.json()['note'] == note


def test_move_project_card(github_request_context, project_column_ids, page, github_username, github_password, github_project_number):
    # Prep a card via API
    now = time.time()
    note = f'Move this card at {now}'
    c_response = github_request_context.post(
        f'/projects/columns/{project_column_ids[0]}/cards',
        data={'note': note})
    assert c_response.ok

    # Login
    page.goto(f'https://github.com/login')
    page.fill('id=login_field', github_username)
    page.fill('id=password', github_password)
    page.click('input[name="commit"]')

    # Load the project page
    page.goto(f'https://github.com/users/{github_username}/projects/{github_project_number}')

    # Move a card via web UI
    page.drag_and_drop(f'text="{note}"', f'id=column-cards-{project_column_ids[1]}')

    # Verify the card is in the new column
    expect(page.locator(f'//div[@id="column-cards-{project_column_ids[1]}"]//p[contains(text(), "{note}")]')).to_be_visible()

    # Verify the backend is updated
    r_response = github_request_context.get(f'/projects/columns/cards/{c_response.json()["id"]}')
    assert r_response.ok
    assert r_response.json()['column_url'].endswith(str(project_column_ids[1]))
