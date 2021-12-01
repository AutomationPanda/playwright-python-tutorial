# Nifty Playwright tricks

Now that we have a complete test case, we can use it to explore some of Playwright's nifty features.
Part 5 of this workshop will explore various things like testing different browsers, capturing images, and running tests in parallel.
Check the [Pytest plugin](https://playwright.dev/python/docs/test-runners) page
in the Playwright docs to learn even more advanced tricks after this workshop.


## Testing different browsers

So far, we have done all of our testing using Chromium, which is the default browser for Playwright.
Testing Firefox and WebKit, the other two browsers bundled with Playwright, is as easy as adding a commmand line option.
Use the `--browser` option with the `pytest-playwright` plugin like this:

```bash
$ python3 -m pytest tests --browser chromium
$ python3 -m pytest tests --browser firefox
$ python3 -m pytest tests --browser webkit
```

Give these a try and see what happens.
You may want to append `--headed --slowmo 1000` so you can actually see the automation at work.

You can also run tests against multiple browsers at the same time.
Just add as many `--browser` options as you want to the same invocation.
Pytest will treat each browser as a test case parameter.
For example, you can run all three browsers like this:

```bash
$ python3 -m pytest tests --browser chromium --browser firefox --browser webkit --verbose
```

The extra `--verbose` option is not necessary,
but adding it will make pytest list each test result with its browser so you can see the parameterization.

Sometimes, for whatever reason, you may want to test against stock browsers on your machine instead of Chromium, Firefox, or WebKit.
Playwright enables you to test Google Chrome and Microsoft Edge through
[browser channels](https://playwright.dev/python/docs/browsers/#google-chrome--microsoft-edge).
Use the `--browser-channel` option like this:

```bash
$ python3 -m pytest tests --browser-channel chrome
$ python3 -m pytest tests --browser-channel msedge
```

Unfortunately, at the time of this workshop (December 2021),
Playright does not support channels for browsers other than Chrome and Edge.

Playwright also allows you to emulate mobile devices to test responsive layouts.
The full list of available devices is
[here](https://github.com/microsoft/playwright/blob/master/packages/playwright-core/src/server/deviceDescriptorsSource.json),
and it's quite long!
To test one of these devices, use the `--device` option like this:

```bash
$ python3 -m pytest tests --device "iPad Mini"
$ python3 -m pytest tests --browser webkit --device "iPhone 11"
$ python3 -m pytest tests --browser chromium --device "Pixel 5"
```

Give it a try with `--headed --slowmo 1000` to see the drastically different screen sizes.



## Capturing screenshots and videos

TBD


## Running tests in parallel

TBD
