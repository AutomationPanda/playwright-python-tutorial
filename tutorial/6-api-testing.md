# Part 6: API testing

Did you know that Playwright has support for built-in
[API testing](https://playwright.dev/python/docs/api-testing)? 
While you could use Playwright for purely testing APIs,
this feature shines when used together with web UI testing.

In this part, we will learn how to use Playwright's API testing features by automating tests
for [GitHub project boards](https://docs.github.com/en/issues/organizing-your-work-with-project-boards).
These tests will be more complex than our previous DuckDuckGo search test.
They will make multiple calls to the [GitHub API](https://docs.github.com/en/rest) with authentication.
The first test will *create* a new project card purely from the GitHub API,
and the second test will *move* a project card from one column to another.


## API setup

Before we can develop tests for GitHub project boards,
we need to set up a few things:

1. A GitHub account
2. A GitHub user project
3. A GitHub personal access token

Pretty much every developer these days already has a GitHub account,
but not every developer may have set up a project board in GitHub.
Follow the [user project instructions](https://docs.github.com/en/issues/organizing-your-work-with-project-boards/managing-project-boards/creating-a-project-board#creating-a-user-owned-project-board)
to create a user project.
Create a "classic" project and not a *Beta* project.
Use the "Basic Kanban" template – the project must have at least two columns.
The project may be public or private,
but I recommend making it private if you intend to use it only for this tutorial.

GitHub API calls require a *personal access token* for authentication.
GitHub no longer supports "basic" authentication with username and password.
Follow the [personal access token instructions](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
to create a personal access token.
Select the **repo** and **user** permissions.
Remember to copy and save your token somewhere safe,
because you won't be able to view it again!

The tests also need the following four inputs:

1. Your GitHub username
2. Your GitHub password (for UI login)
3. Your GitHub personal access token (for API authentication)
4. Your GitHub user project name

Let's set these inputs as environment variables
and read them into tests using pytest fixtures.
Environment variables must be set before launching tests.

On macOS or Linxu, use the following commands:

```bash
$ export GITHUB_USERNAME=<github-username>
$ export GITHUB_PASSWORD=<github-password>
$ export GITHUB_ACCESS_TOKEN=<github-access-token>
$ export GITHUB_PROJECT_NAME="<github-project-name>"
```

On Windows:

```console
> set GITHUB_USERNAME=<github-username>
> set GITHUB_PASSWORD=<github-password>
> set GITHUB_ACCESS_TOKEN=<github-access-token>
> set GITHUB_PROJECT_NAME="<github-project-name>"
```

> *Warning:*
> Make sure to keep these values secure.
> Do not share your password or access token with anyone.

We should read these environment variables through pytest fixtures
using the [`os`](https://docs.python.org/3/library/os.html) module
so that any test can easily access them.
Add the following function for reading environment variables to `tests/conftest.py`:

```python
import os

def _get_env_var(varname):
    value = os.getenv(varname)
    assert value, f'{varname} is not set'
    return value
```

This function will not only read an environment variable by name
but also make sure the variable has a value.
Then, add fixtures for each environment variable:

```python
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
```

Now, our tests can safely and easily fetch these variables.
These fixtures have *session* scope so that pytest will read them only one time during the entire testing session.


## Writing a pure API test

?


## Writing a hybrid UI/API test

?
