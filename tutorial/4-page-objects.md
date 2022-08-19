# Part 4: Refactoring using page objects

As we saw in the previous part, Playwright calls are wonderfully concise.
We may be tempted to use raw Playwright calls in all our tests.
However, raw calls quickly lead to code duplication.

In this part, we will refactor our DuckDuckGo search test using the
[Page Object Model](https://www.selenium.dev/documentation/guidelines/page_object_models/) (POM).
Page objects, though imperfect, provide decent structure and helpful reusability.
They are superior to raw Playwright calls when automating multiple tests instead of only one script.


## The search page

Our search tests interacts with two pages:

1. The DuckDuckGo search page
2. The DuckDuckGo result page

Each page should be modeled by its own class.
Page object classes should be located in a package outside of the `tests` directory so that they can be imported by tests.

Create a new directory named `pages`, and inside it, create blank files with the following names:

* `__init__.py`
* `search.py`
* `result.py`

Your project's directory layout should look like this:

```
playwright-python-tutorial
├── pages
│   ├── __init__.py
│   ├── search.py
│   └── result.py
└── tests
    └── test_search.py
```

The `__init__.py` file turns the `pages` directory into a Python package so that other Python modules can import it.
It will stay permanently empty.
The `search.py` and `result.py` modules will contain the search and result page object classes respectively.

Let's implement the search page first.
We will use much of our original code.

A page object class typically has three main parts:

1. Dependency injection of the browser automator through a constructor
2. Locators and any other data stored as variables
3. Interaction methods that use the browser automator and the selectors

Let's add these one at a time.
Inside `pages/search.py`, import Playwright's `Page` class:

```python
from playwright.sync_api import Page
```

Add a class definition for the page object:

```python
class DuckDuckGoSearchPage:
```

Inside this class, add the DuckDuckGo URL:

```python
    URL = 'https://www.duckduckgo.com'
```

> *Warning:*
> Base URLs should typically be passed into automation code as an input, not hard-coded in a page object.
> We are doing this here as a matter of simplicity for this tutorial.

Next, let's handle dependency injection for the browser automator.
Since each test will have its own Playwright page, we should inject that page.
(If we were using Selenium WebDriver, then we would inject the WebDriver instance.)
Add the following initializer method to the class:

```python
    def __init__(self, page: Page) -> None:
        self.page = page
```

The `__init__` method is essentially a constructor for Python classes
(but with a bit of nuance that doesn't matter for this tutorial).
It has one argument named `page` for the Playwright page,
which it stores as an instance variable (via `self`).

Let's also add locators for search page elements to the constructor.
Our test needs locators for the search button and the search input:

```python
        self.search_button = page.locator('#search_button_homepage')
        self.search_input = page.locator('#search_form_input_homepage')
```

These locators are created once and can be used anywhere.
We can use them to make interactions.

One interaction our test performs is loading the DuckDuckGo search page.
Here's a method to do that:

```python
    def load(self) -> None:
        self.page.goto(self.URL)
```

It uses the injected page as well as the `URL` variable.

The other interaction our test performs is searching for a phrase.
Here's a method to do that:

```python
    def search(self, phrase: str) -> None:
        self.search_input.fill(phrase)
        self.search_button.click()
```

This `search` method uses the page objects to perform the search.
It also takes in the search phrase as an argument so that it can handle any phrase.

The completed search page object class should look like this:

```python
from playwright.sync_api import Page

class DuckDuckGoSearchPage:

    URL = 'https://www.duckduckgo.com'

    def __init__(self, page: Page) -> None:
        self.page = page
        self.search_button = page.locator('#search_button_homepage')
        self.search_input = page.locator('#search_form_input_homepage')
    
    def load(self) -> None:
        self.page.goto(self.URL)
    
    def search(self, phrase: str) -> None:
        self.search_input.fill(phrase)
        self.search_button.click()
```

We can now refactor the original test case to use this new page object!
Replace this old code:

```python
def test_basic_duckduckgo_search(page: Page) -> None:
    
    # Given the DuckDuckGo home page is displayed
    page.goto('https://www.duckduckgo.com')

    # When the user searches for a phrase
    page.locator('#search_form_input_homepage').fill('panda')
    page.locator('#search_button_homepage').click()
```

With this new code:

```python
from pages.search import DuckDuckGoSearchPage

def test_basic_duckduckgo_search(page: Page) -> None:
    search_page = DuckDuckGoSearchPage(page)
    
    # Given the DuckDuckGo home page is displayed
    search_page.load()

    # When the user searches for a phrase
    search_page.search('panda')
```

The new code must import `DuckDuckGoSearchPage` from the `pages.search` module.
The test then constructs a `DuckDuckGoSearchPage` object and uses it to perform interactions.
Notice that the test case no longer has hard-coded selectors or URLs.
The code is also more self-documenting.

Rerun the test (`python3 -m pytest tests --headed --slowmo 1000`).
The test should pass.
Nothing has functionally changed for the test:
it still performs the same operations.
Now, it just uses a page object for the search page instead of raw calls.


## The result page

After writing the search page class, the result page class will be straightforward.
It will follow the same structure.
The main difference is that each interaction method in the result page class will return a value
because test assertions will check page values.

Start by adding the following imports for type checking to `pages/result.py`:

```python
from playwright.sync_api import Page
from typing import List
```

Add the class definition:

```python
class DuckDuckGoResultPage:
```

Add dependency injection with locators:

```python
    def __init__(self, page: Page) -> None:
        self.page = page
        self.result_links = page.locator('a[data-testid="result-title-a"]')
        self.search_input = page.locator('#search_form_input')
```

Now, let's add interaction methods.
Since the verifications for the search input and title are simple,
we don't need new methods for those.
The test case function can call the `search_input` locator and the `page` object directly for those.
However, the verification for search result links has some complex code
that should be handled within the page object.
We can break this down into two methods:

1. A method to get all result link titles as a list.
2. A method to check if the list of result link titles contains a phrase.

Add the following methods to the class:

```python
    def result_link_titles(self) -> List[str]:
        self.result_links.nth(4).wait_for()
        return self.result_links.all_text_contents()
    
    def result_link_titles_contain_phrase(self, phrase: str, minimum: int = 1) -> bool:
        titles = self.result_link_titles()
        matches = [t for t in titles if phrase.lower() in t.lower()]
        return len(matches) >= minimum
```

In the first method, the `result_links` locator is used twice.
The first time it is called,
it is concatenated with the N-th element fetcher to wait for at least 5 elements to appear.
The second time it is called,
it gets all the text contents for the elements it finds.

The second method takes in a search phrase and a minimum limit for matches.
It calls the first method to get the list of titles,
filters the titles using a list comprehension,
and returns a Boolean value indicating if the number of matches meets the minimum threshold.
Notice that this method does **not** perform an assertion.
Assertions should *not* be done in page objects.
They should only be done in test cases.

The full code for `pages/result.py` should look like this
(after rearranging methods alphabetically):

```python
from playwright.sync_api import Page
from typing import List

class DuckDuckGoResultPage:

    def __init__(self, page: Page) -> None:
        self.page = page
        self.result_links = page.locator('a[data-testid="result-title-a"]')
        self.search_input = page.locator('#search_form_input')
    
    def result_link_titles(self) -> List[str]:
        self.result_links.nth(4).wait_for()
        return self.result_links.all_text_contents()
    
    def result_link_titles_contain_phrase(self, phrase: str, minimum: int = 1) -> bool:
        titles = self.result_link_titles()
        matches = [t for t in titles if phrase.lower() in t.lower()]
        return len(matches) >= minimum
```

After rewriting the original test case to use `DuckDuckGoResultPage`,
the code in `tests/test_search.py` should look like this:

```python
from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage
from playwright.sync_api import expect, Page

def test_basic_duckduckgo_search(page: Page) -> None:
    search_page = DuckDuckGoSearchPage(page)
    result_page = DuckDuckGoResultPage(page)

    # Given the DuckDuckGo home page is displayed
    search_page.load()

    # When the user searches for a phrase
    search_page.search('panda')

    # Then the search result query is the phrase
    expect(result_page.search_input).to_have_value('panda')

    # And the search result links pertain to the phrase
    assert result_page.result_link_titles_contain_phrase('panda')

    # And the search result title contains the phrase
    expect(page).to_have_title('panda at DuckDuckGo')
```

These calls look less "code-y" than the raw Playwright calls.
They read much more like a test case.

Rerun the test again to make sure everything is still working.


## Page object fixtures

There is one more thing we can do to maximize the value of our new page objects:
we can create fixtures to automatically construct them!
In our current test, we construct them explicitly inside the test function.
If we add more test functions in the future, that construction code will become repetitive.
Page object fixtures will help our code stay concise.

In pytest, shared fixtures belong in a module under the `tests` directory named `conftest.py`.
Create a new file at `tests/conftest.py`.
The new project directory layout should look like this:

```
playwright-python-tutorial
├── pages
│   ├── __init__.py
│   ├── search.py
│   └── result.py
└── tests
    ├── conftest.py
    └── test_search.py
```

Then, add the following code to `tests/conftest.py`:

```python
import pytest

from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage
from playwright.sync_api import Page

@pytest.fixture
def result_page(page: Page) -> DuckDuckGoResultPage:
    return DuckDuckGoResultPage(page)

@pytest.fixture
def search_page(page: Page) -> DuckDuckGoSearchPage:
    return DuckDuckGoSearchPage(page)
```

The two fixtures, `result_page` and `search_page`,
each call the Playwright `page` fixture and use it to construct a page object.
Just like `page`, they have function scope.
If both page object fixtures are called for the same test
(like we will do for `test_basic_duckduckgo_search`),
then they will both receive the same `page` object due to fixture scope.
You can learn more about fixtures from the
[pytest fixtures](https://docs.pytest.org/en/6.2.x/fixture.html) doc page.

To use these new fixtures, rewrite `tests/test_search.py` like this:

```python
from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage
from playwright.sync_api import expect, Page

def test_basic_duckduckgo_search(
    page: Page,
    search_page: DuckDuckGoSearchPage,
    result_page: DuckDuckGoResultPage) -> None:
    
    # Given the DuckDuckGo home page is displayed
    search_page.load()

    # When the user searches for a phrase
    search_page.search('panda')

    # Then the search result query is the phrase
    expect(result_page.search_input).to_have_value('panda')

    # And the search result links pertain to the phrase
    assert result_page.result_link_titles_contain_phrase('panda')

    # And the search result title contains the phrase
    expect(page).to_have_title('panda at DuckDuckGo')
```

Notice a few things:

* The `search_page` and `result_page` fixtures are declared as arguments for the test function.
* The test function no longer explicitly constructs page objects.
* Each test step is only one line long.

If you use page objects, then **all interactions should be performed using page objects**.
It is not recommended to mix raw Playwright calls (except `expect` assertions) with page object calls.
That becomes confusing, and it encourages poor practices like dirty hacks and copypasta.
It also causes a test automation project to lose strength from a lack of conformity in design.

Rerun the test one more time to make sure the fixtures work as expected.
Congratulations!
You have finished refactoring this test case using page objects.
