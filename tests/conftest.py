"""
This module contains shared fixtures.
"""

import pytest

from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage


@pytest.fixture
def result_page(page):
    return DuckDuckGoResultPage(page)


@pytest.fixture
def search_page(page):
    return DuckDuckGoSearchPage(page)