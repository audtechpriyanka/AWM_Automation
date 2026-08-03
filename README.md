# AWM UAT Automation Framework

Playwright + Pytest automation framework for the AWM (Audit Workflow
Management) UAT application, built on a self-healing Page Object Model.

This is a Playwright + Pytest automation framework for the AWM (Audit
Workflow Management) UAT application, built on a self-healing Page Object
Model. Login, dashboard/logout, client + assignment management, and core
assignment-workspace flows (materiality, checklist, trial balance,
sign-off menu, templates, etc.) are implemented. See
[`AGENT_GUIDE.md`](./AGENT_GUIDE.md) for how to extend coverage further.

## Structure

```
src/
  config/settings.py       # all config — reads from .env, single source of truth
  utilities/
    logger.py              # get_logger(__name__) — writes to logs/
    screenshots.py         # capture_screenshot(page, label) — writes to screenshots/, attaches to Allure
    self_healing.py         # resolve_locator() + @self_heal() retry decorator
  locators/                # ordered fallback locator strategies per feature
  pages/                   # BasePage + feature page objects
  tests/
    conftest.py             # PageManager, browser/context config, screenshot-on-failure hook
    login_test/
    dashboard_test/
    client_test/
    assignment_test/
    workflow_test/          # assignment workspace / audit screens
    profile_test/
reports/
  allure-results/          # raw results (generated)
  allure-report/           # generated HTML report (needs Allure CLI + Java)
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

- **Allure HTML report generation** requires a local Java runtime (`JAVA_HOME`)
  plus the Allure CLI. `allure-pytest` already writes raw results under
  `reports/allure-results/` on every run; `make report` / `make report-serve`
  will fail until Java + Allure CLI are installed (see Setup above).
- **Create Client** coverage exercises the Basic Info step (load, required-field
  guard, name boundary) — it does **not** submit a full 4-step client create
  end-to-end, to avoid polluting UAT with throwaway orgs.
- **Create Assignment** coverage validates form load, disabled CREATE when
  empty, and AWM type selection — it does **not** persist a new assignment
  (dates / EPR / Audit Pack prerequisites are assignment-specific).
- **Audit workflow** tests open a known UAT assignment
  (`KNOWN_ASSIGNMENT_NAME`, default `Test AWMS_295 3.08.2026`) and navigate
  Materiality, Planning Checklist, Risk Database, Budget, Trial Balance,
  Templates, Client Queries, Audit Journal, Sampling, and Sign-Off menu.
  Nested submenu items under B3/B4/C* that use `navigate_next` (no direct
  href) are not deep-linked yet.
- **Data analytics / system documents / download report** are not covered as
  dedicated modules — Templates + Sign-Off menu are the reporting surface
  exercised so far; expand if those screens are required.
- **Independence / Declaration** post-login redirect is intermittent on UAT;
  smoke login currently lands on `#/dashboard` for this account but may
  occasionally route through `#/independence/fill-template`.
- No CI workflow file included yet (add `.github/workflows/` once desired).
