# Part 1: Getting started

Part 1 of the tutorial explains how to set up a Python test automation project with pytest and Playwright.


## What is Playwright?

[Playwright](https://playwright.dev/python/) is a new library that can automate interactions with Chromium, Firefox, and WebKit browsers via a single API.
It is an open source project developed by Microsoft.

Playwright is a fantastic alternative to [Selenium WebDriver](https://www.selenium.dev/) for web UI testing.
Like Selenium WebDriver, Playwright has language bindings in multiple languages: Python, .NET, Java, and JavaScript.
Playwright also refines many of the pain points in Selenium WebDriver.
Some examples include:

* Playwright interactions automatically wait for elements to be ready.
* Playwright can use one browser instance with multiple browser contexts for isolation instead of requiring multiple instances.
* Playwright has device emulation for testing responsive web apps in mobile browsers.

For a more thorough list of advantages, check out
[Why Playwright?](https://playwright.dev/python/docs/why-playwright/)
from the docs.


## Our web search test

For this tutorial, we will walk through one test scenario for DuckDuckGo searching.
[DuckDuckGo](https://duckduckgo.com/) is a search engine like Google or Yahoo.

The steps for a basic DuckDuckGo search are:

```gherkin
Given the DuckDuckGo home page is displayed
When the user searches for a phrase
Then the search result query is the phrase
And the search result links pertain to the phrase
And the search result title contains the phrase
```

Go to [duckduckgo.com](https://duckduckgo.com/) and give this a try.
You can use any search phrase you like.
It is important to write a test *case* before writing test *code*.
It is also important to try a test manually before attempting to automate it.


## Test project setup

Let's set up the test project!
For this tutorial, we will build a new project from the ground up.
The GitHub repository should be used exclusively as a reference for example code.

Create a directory named `playwright-python-tutorial` for the project:

```bash
$ mkdir playwright-python-tutorial
$ cd playwright-python-tutorial
```

Inside this project, create a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html)
using the [venv](https://docs.python.org/3/library/venv.html) module
to manage dependency packages locally:

```bash
$ python3 -m venv venv
```

Creating a new virtual environment for each Python project is a recommended practice.
This command will create a subdirectory named `venv` that holds all virtual environment files, including dependency packages.

*A note about Python commands:*
Python has two incompatible major versions: 2 and 3.
Although Python 2 end-of-life was January 1, 2020, many machines still run it.
For example, macOS comes bundled with Python 2.7.18.
Sometimes, the `python` executable may point to Python 2 instead of 3.
To be precise about versions and executables, we will use the `python3` and `pip3` commands explicitly in this tutorial.

After creating a virtual environment, you must "activate" it.
On macOS or Linux, use the following command:

```bash
$ source venv/bin/activate
```

The equivalent command for a Windows command line is:

```
> venv\Scripts\activate.bat
```

You can tell if a virtual environment is active if its name appears in the prompt.

Let's add some Python packages to our new virtual environment:

```bash
$ pip3 install playwright
$ pip3 install pytest
$ pip3 install pytest-playwright
```

> If you want to run the tests from this repository instead of creating a fresh project,
> install the dependencies using this command:
>  
> `$ pip3 install -r requirements.txt`

By itself, Playwright is simply a library for browser automation.
We need a test framework like pytest if we want to automate tests.
The [`pytest-playwright`](https://playwright.dev/python/docs/test-runners)
is a pytest plugin developed by the Playwright team that simplifies Playwright integration.

You can check all installed packages using `pip3 freeze`.
They should look something like this:

```bash
$ pip3 freeze
attrs==21.2.0
certifi==2021.10.8
charset-normalizer==2.0.8
greenlet==1.1.2
idna==3.3
iniconfig==1.1.1
packaging==21.3
playwright==1.19.1
pluggy==1.0.0
py==1.11.0
pyee==8.1.0
pyparsing==3.0.6
pytest==7.0.1
pytest-base-url==1.4.2
pytest-playwright==0.2.3
python-slugify==5.0.2
requests==2.26.0
text-unidecode==1.3
toml==0.10.2
tomli==2.0.1
urllib3==1.26.7
websockets==10.1
```

Notice that pip fetches dependencies of dependencies.
It is customary for Python projects to store this list of dependencies in a file named `requirements.txt`.

After the Python packages are installed, we need to install the browsers for Playwright.
The `playwright install` command installs the latest versions of the three browsers that Playwright supports:
Chromium, Firefox, and WebKit:

```bash
$ playwright install
```

By default, pytest with the Playwright plugin will run headless Chromium.
We will show how to run against other browsers in Part 5.

Finally, let's create a test function stub.
By Python conventions, all tests should be located under a `tests` directory.
Create a `tests` directory, and inside, create a file named `test_search.py`:

```bash
$ mkdir tests
$ touch tests/test_search.py
```

Add the following code to `tests/test_search.py`:

```python
def test_basic_duckduckgo_search() -> None:
    # Given the DuckDuckGo home page is displayed
    # When the user searches for a phrase
    # Then the search result query is the phrase
    # And the search result links pertain to the phrase
    # And the search result title contains the phrase
    pass
```

The `test_basic_duckduckgo_search` is merely a stub, but it establishes good practices:

* It has a clear name.
* It defines the behavior to test step-by-step in its comments.
* It can be run immediately.

The `pass` statement at the end is just a no-op.
It does **not** mean "pass the test".

Remember, write test *cases* before you write test *code*.

Before continuing, run this test to make sure everything is set up correctly:

```bash
$ python3 -m pytest tests
```

pytest should discover, run, and pass the single test case under the `tests` directory.

*A note about the pytest command:*
Many online articles and examples use the `pytest` command directly to run tests, like this: `pytest tests`.
Unfortunately, this version of the command does **not** add the current directory to the Python path.
If your tests reference anything outside of their test modules, then the command will fail.
Therefore, I always recommend running the full `python3 -m pytest tests` command.
