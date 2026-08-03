# AWM UAT Automation Framework

Playwright + Pytest automation framework for the AWM (Audit Workflow
Management) UAT application, built on a self-healing Page Object Model.

This is a **lean starter skeleton**, not a full test suite. It ships with
a working, fully-implemented Login flow as the reference pattern. See
[`AGENT_GUIDE.md`](./AGENT_GUIDE.md) for how to explore the live app and
expand coverage feature by feature — that file is written as direct
instructions for an AI coding agent (e.g. Cursor) with live browser access.

## Structure

```
src/
  config/settings.py       # all config — reads from .env, single source of truth
  utilities/
    logger.py              # get_logger(__name__) — writes to logs/
    screenshots.py         # capture_screenshot(page, label) — writes to screenshots/, attaches to Allure
    self_healing.py         # resolve_locator() + @self_heal() retry decorator
  locators/
    login_locators.py      # example: ordered fallback locator strategies per element
  pages/
    base_page.py           # shared safe_click/safe_fill/expect_* — inherit this
    login_page.py           # reference implementation
    dashboard_page.py       # stub — expand as you explore
  tests/
    conftest.py             # PageManager, browser/context config, screenshot-on-failure hook
    login_test/test_login.py
reports/
  allure-results/          # raw results (generated)
  allure-report/           # generated HTML report
screenshots/               # captured on every failure + key steps
logs/automation.log        # full run log
```

## Setup

```bash
cp .env.example .env
# fill in BASE_URL, VALID_USERNAME, VALID_PASSWORD, etc. in .env

make install
```

Allure's report generator is a separate CLI (Java-based), not a pip
package — `allure-pytest` only writes the raw results. Install it via:

```bash
# macOS
brew install allure
# or via npm
npm install -g allure-commandline
```

## Running tests

```bash
make test               # headless run, writes reports/allure-results/
make test-headed        # watch it run
make test-tag TAG=smoke # run only tests marked @pytest.mark.smoke
make report-serve       # generate + open the Allure HTML report
```

Logs land in `logs/automation.log`. Screenshots for every failure (and
key steps like pre/post sign-in) land in `screenshots/`.

## Markers

`smoke`, `regression`, `positive`, `negative`, `exploratory` — defined in
`pytest.ini`. Tag every new test with at least one.

## Self-healing model

- **Locators** are defined as ordered fallback lists in `src/locators/*.py`
  (see `login_locators.py`). `BasePage.resolve()` tries each in order and
  logs a warning when a fallback had to be used — check
  `logs/automation.log` for `Locator fallback used for ...` to find
  selectors that need the primary promoted.
- **Actions** (`safe_click`, `safe_fill`, `safe_select`, `safe_upload`)
  are wrapped with `@self_heal()`, which retries on failure with backoff
  and captures a screenshot + log entry on every attempt. This handles
  timing/flakiness, not structural app changes — a genuinely broken
  locator still needs a source fix in `src/locators/`.
- On any test failure, `conftest.py`'s `pytest_runtest_makereport` hook
  captures a screenshot and logs the failing URL automatically.

## Known limitations

- Only Login is fully implemented. Every other AWM module (dashboard nav,
  clients, assignments, checklists, trial balance, sign-off, etc.) needs
  its locator file + page object + test module built out — see
  `AGENT_GUIDE.md`.
- `DashboardPage.logout()` is a stub — the logout control location wasn't
  confirmed against the current app build.
- No CI workflow file included yet (add `.github/workflows/` once the
  suite has enough coverage to be worth gating on).
