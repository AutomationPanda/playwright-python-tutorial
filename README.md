# tau-playwright-workshop

This repository contains the instructions and example code for the Playwright workshop
for [TAU: The Homecoming](https://applitools.com/tau-homecoming/)
on December 1, 2021.
The workshop will be done in [Python](python.org).


## Instructions

Please try to attend the workshop *live* on the day of the event.
However, if you cannot make it, never fear!
**You can still take the workshop as a self-guided tutorial.**
Start by reading this README.
Then, follow the guides in the `workshop` folder.
Each part of the workshop has a `workshop` guide with full instructions.
Feel free to open issues against this repository if you have any trouble completing the workshop independently.


## Abstract

[Playwright](https://playwright.dev/python/)
is a hot new browser automation tool from Microsoft.
With bindings for .NET, Java, JavaScript, and Python, it’s a strong alternative to Selenium WebDriver for end-to-end web app testing.

This workshop will be an introduction to Playwright using [Python](python.org).
We will automate a test scenario together that performs a [DuckDuckGo](https://duckduckgo.com/) search.
As we code along the test together, we will learn:

* How to install and configure Playwright
* How to integrate Playwright with [pytest](pytest.org), Python’s leading test framework
* How to perform interactions through page objects
* How to conveniently run different browsers, capture videos, and run tests in parallel

Come prepared with Python 3.7 or higher installed on your machine.
By the end of the workshop, you will have a solid foundation in Playwright as well as a Python project you can extend with new tests!


## Prerequisites

To code along with this workshop, your machine must have Python 3.7 or higher.
You should also have a decent Python editor like
[Visual Studio Code](https://code.visualstudio.com/docs/languages/python)
or [PyCharm](https://www.jetbrains.com/pycharm/).

The command line shown in examples below is [bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)).
If you are using a different shell or a Windows command line, some commands may need to be different.


## Agenda

This workshop has five main parts, each with three sections:

1. Getting started
   1. What is Playwright?
   2. Our web search test
   3. Test project setup
2. First steps with Playwright
   1. Browsers, contexts, and pages
   2. Navigating to a web page
   3. Performing a search
3. Writing assertions
   1. Checking the search field
   2. Checking the result links
   3. Checking the title
4. Refactoring using page objects
   1. The search page
   2. The result page
   3. Page object fixtures
5. Nifty Playwright tricks
   1. Testing different browsers
   2. Capturing screenshots and videos
   3. Running tests in parallel


## Example code branches

Each workshop part has a corresponding branch in this repository containing the part's example code and `workshop` instructions.
The branches allow you to check your progress at any point during the workshop.
The branch names are:

| Part     | Branch              |
| ------   | ------------------- |
| Start    | 0-initial-project   |
| Part 1   | 1-getting-started   |
| Part 2   | 2-first-steps       |
| Part 3   | 3-assertions        |
| Part 4   | 4-page-objects      |
| Part 5   | 5-playwright-tricks |
| Complete | main                |