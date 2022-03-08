"""
This module contains shared fixtures.
"""

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------

import os
import pytest


# ------------------------------------------------------------
# DuckDuckGo search fixtures
# ------------------------------------------------------------

from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage


@pytest.fixture
def result_page(page):
    return DuckDuckGoResultPage(page)


@pytest.fixture
def search_page(page):
    return DuckDuckGoSearchPage(page)


# ------------------------------------------------------------
# GitHub project fixtures
# ------------------------------------------------------------

# Environment variables

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


# Request context

@pytest.fixture(scope='session')
def gh_context(playwright, gh_access_token):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {gh_access_token}"}

    request_context = playwright.request.new_context(
        base_url="https://api.github.com",
        extra_http_headers=headers)

    yield request_context
    request_context.dispose()


# GitHub project requests

@pytest.fixture(scope='session')
def gh_project(gh_context, gh_username, gh_project_name):
    resource = f'/users/{gh_username}/projects'
    response = gh_context.get(resource)
    assert response.ok
    
    name_match = lambda x: x['name'] == gh_project_name
    filtered = filter(name_match, response.json())
    project = list(filtered)[0]
    assert project

    return project


@pytest.fixture()
def project_columns(gh_context, gh_project):
    response = gh_context.get(gh_project['columns_url'])
    assert response.ok

    columns = response.json()
    assert len(columns) >= 2
    return columns


@pytest.fixture()
def project_column_ids(project_columns):
    return list(map(lambda x: x['id'], project_columns))
