# Refactoring using page objects

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
tau-playwright-workshop
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

1. Selectors and any other data stored as variables
2. Dependency injection of the browser automator through a constructor
3. Interaction methods that use the browser automator and the selectors

Let's add these one at a time.
Inside `pages/search.py`, add a class definition for the page object:

```python
class DuckDuckGoSearchPage:
```

Inside this class, add the selectors we used in our test for the search input and search button:

```python
    SEARCH_BUTTON = '#search_button_homepage'
    SEARCH_INPUT = '#search_form_input_homepage'
```

These will be class variables, not instance variables.
They are also plain-old strings.
We could use these selectors for many different actions.

Let's also add the DuckDuckGo URL:

```python
    URL = 'https://www.duckduckgo.com'
```

*(Warning:
Base URLs should typically be passed into automation code as an input, not hard-coded in a page object.
We are doing this here as a matter of simplicity for this workshop.)*

Next, let's handle dependency injection for the browser automator.
Since each test will have its own Playwright page, we should inject that page.
(If we were using Selenium WebDriver, then we would inject the WebDriver instance.)
Add the following initializer method to the class:

```python
    def __init__(self, page):
        self.page = page
```

The `__init__` method is essentially a constructor for Python classes
(but with a bit of nuance that doesn't matter for this workshop).
It has one argument named `page` for the Playwright page,
which it stores as an instance variable (via `self`).

With the page injected, we can now use it to make interactions.
One interaction our test performs is loading the DuckDuckGo search page.
Here's a method to do that:

```python
    def load(self):
        self.page.goto(self.URL)
```

It uses the injected page as well as the `URL` variable.

The other interaction our test performs is searching for a phrase.
Here's a method to do that:

```python
    def search(self, phrase):
        self.page.fill(self.SEARCH_INPUT, phrase)
        self.page.click(self.SEARCH_BUTTON)
```

This `search` method uses the injected page and the selector variables.
It also takes in the search phrase as an argument so that it can handle any phrase.

The completed search page object class should look like this:

```python
class DuckDuckGoSearchPage:

    SEARCH_BUTTON = '#search_button_homepage'
    SEARCH_INPUT = '#search_form_input_homepage'

    URL = 'https://www.duckduckgo.com'

    def __init__(self, page):
        self.page = page
    
    def load(self):
        self.page.goto(self.URL)
    
    def search(self, phrase):
        self.page.fill(self.SEARCH_INPUT, phrase)
        self.page.click(self.SEARCH_BUTTON)
```

This diagram shows how each section of this class fits the standard sections of a page object class:

![Page object structure](images/page-object-structure.png)

We can now refactor the original test case to use this new page object!
Replace this old code:

```python
def test_basic_duckduckgo_search(page):

    # Given the DuckDuckGo home page is displayed
    page.goto('https://www.duckduckgo.com')

    # When the user searches for a phrase
    page.fill('#search_form_input_homepage', 'panda')
    page.click('#search_button_homepage')
```

With this new code:

```python
from pages.search import DuckDuckGoSearchPage

def test_basic_duckduckgo_search(page):
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
The main difference is that each interaction methods in the result page class will return a value
because test assertions will check page values.

Start by adding the class definition to `pages/result.py`:

```python
class DuckDuckGoResultPage:
```

Add the selectors we used in the test case:

```python
    RESULT_LINKS = '.result__title a.result__a'
    SEARCH_INPUT = '#search_form_input'
```

Add dependency injection:

```python
    def __init__(self, page):
        self.page = page
```

Now, let's add interaction methods for all the things assertions must check.
The first assertion checked the input value of the search input.
Let's add a method to get and return that input value:

```python
    def search_input_value(self):
        return self.page.input_value(self.SEARCH_INPUT)
```

The second assertion was the most complex.
It checked if at least one result link title contained the search phrase.
We can break this down into two methods:

1. A method to get all result link titles as a list.
2. A method to check if the list of result link titles contains a phrase.

Add the following methods to the class:

```python
    def result_link_titles(self):
        self.page.locator(f'{self.RESULT_LINKS} >> nth=4').wait_for()
        titles = self.page.locator(self.RESULT_LINKS).all_text_contents()
        return titles
    
    def result_link_titles_contain_phrase(self, phrase, minimum=1):
        titles = self.result_link_titles()
        matches = [t for t in titles if phrase.lower() in t.lower()]
        return len(matches) >= minimum
```

In the first method, the `RESULT_LINKS` selector is used twice.
The first time it is used, it is concatenated with the N-th element selector using an
[f-string](https://realpython.com/python-f-strings/).

The second method takes in a search phases and a minimum limit for matches.
It calls the first method to get the list of titles,
filters the titles using a list comprehension,
and returns a Boolean value indicating if the number of matches meets the minimum threshold.
Notice that this method does **not** perform an asssertion.
Assertions should *not* be done in page objects.
They should only be done in test cases.

The third assertion checked the page title.
Let's add one final method to the result page class to get the title:

```python
    def title(self):
        return self.page.title()
```

The full code for `pages/result.py` should look like this
(after rearranging methods alphabetically):

```python
class DuckDuckGoResultPage:

    RESULT_LINKS = '.result__title a.result__a'
    SEARCH_INPUT = '#search_form_input'
    
    def __init__(self, page):
        self.page = page
    
    def result_link_titles(self):
        self.page.locator(f'{self.RESULT_LINKS} >> nth=4').wait_for()
        titles = self.page.locator(self.RESULT_LINKS).all_text_contents()
        return titles
    
    def result_link_titles_contain_phrase(self, phrase, minimum=1):
        titles = self.result_link_titles()
        matches = [t for t in titles if phrase.lower() in t.lower()]
        return len(matches) >= minimum

    def search_input_value(self):
        return self.page.input_value(self.SEARCH_INPUT)
    
    def title(self):
        return self.page.title()
```

After rewriting the original test case to use `DuckDuckGoResultPage`,
the code in `tests/test_search.py` should look like this:

```python
from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage

def test_basic_duckduckgo_search(page):
    search_page = DuckDuckGoSearchPage(page)
    result_page = DuckDuckGoResultPage(page)

    # Given the DuckDuckGo home page is displayed
    search_page.load()

    # When the user searches for a phrase
    search_page.search('panda')

    # Then the search result query is the phrase
    assert 'panda' == result_page.search_input_value()

    # And the search result links pertain to the phrase
    assert result_page.result_link_titles_contain_phrase('panda')

    # And the search result title contains the phrase
    assert 'panda' in result_page.title()
```

These calls look less "code-y" than the raw Playwright calls.
They read much more like a test case.

Rerun the test again to make sure everything is still working.


## Page object fixtures
