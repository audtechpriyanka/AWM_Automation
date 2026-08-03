# AWM UAT Automation Framework

Playwright + Pytest automation framework for the AWM (Audit Workflow
Management) UAT application, built on a self-healing Page Object Model.

See [`AGENT_GUIDE.md`](./AGENT_GUIDE.md) for how to explore the live app and
extend coverage. Login is the reference pattern every other page object
follows.

## Structure

```
src/
  config/settings.py
  utilities/               # logger, screenshots, self-healing
  locators/                # login, dashboard, client, assignment, workspace
  pages/                   # BasePage + feature page objects
  tests/
    conftest.py            # PageManager, browser config, screenshot-on-failure
    login_test/
    dashboard_test/
    client_test/
    assignment_test/
    workflow_test/         # assignment workspace: materiality, TB, sign-off, …
    profile_test/
reports/
  allure-results/          # raw results (written by pytest)
  allure-report/           # HTML report (needs Allure CLI + Java)
screenshots/
logs/automation.log
```

## Setup

```bash
cp .env.example .env
# fill in BASE_URL, VALID_USERNAME, VALID_PASSWORD
# optional: KNOWN_CLIENT_NAME, KNOWN_ASSIGNMENT_NAME for workspace tests

make install
```

Allure's report generator is a separate CLI (Java-based), not a pip
package — `allure-pytest` only writes the raw results. Install it via:

```bash
# macOS
brew install allure
# or via npm (also requires a working Java/JAVA_HOME)
npm install -g allure-commandline
```

## Running tests

```bash
make test               # headless run, writes reports/allure-results/
make test-headed        # watch it run
make test-tag TAG=smoke # run only tests marked @pytest.mark.smoke
make report             # allure generate … (needs Allure CLI + Java)
make report-serve       # generate + open the Allure HTML report
```

Latest full run (2026-08-03): **39 passed**.

## Markers

`smoke`, `regression`, `positive`, `negative`, `exploratory` — defined in
`pytest.ini`. Tag every new test with at least one.

## Self-healing model

- **Locators** are ordered fallback lists in `src/locators/*.py`.
  `BasePage.resolve()` tries each in order and logs when a fallback is used.
- **Actions** (`safe_click`, `safe_fill`, …) use `@self_heal()` for timing
  retries; broken selectors still need a source fix in the locators file.
- Failures auto-capture a screenshot via `conftest.py`.

## Coverage (current)

| Area | What’s covered |
|------|----------------|
| Login | Valid / invalid / empty / old password |
| Dashboard | Logout, user menu, sidenav Client/Assignment routes |
| Client | Search by name, empty search, create form load + required-field guard + name boundary |
| Assignment | List/filter/search, create form load, CREATE disabled when empty, AWM type select |
| Workspace | Open known AWM assignment; Materiality, Planning Checklist, Risk DB, Budget; header Trial Balance / Templates / Client Queries / Audit Journal / Sampling; Sign-Off menu |
| Profile | Profile + Change Password from user menu |

## Known limitations

- **Allure HTML report not generated on this machine** — `reports/allure-results/`
  is populated by pytest, but `make report` needs the Allure CLI **and** a
  working Java (`JAVA_HOME`). Neither was available in the last run
  environment. Install Java + Allure, then re-run `make report`.
- **Full multi-step create flows are not automated** — Create Client stops at
  Basic Info validation; Create Assignment does not submit a full AWM
  engagement (dates/assignee/audit pack/cleanup). Doing so would mutate shared
  UAT data without a guaranteed cleanup path.
- **Nested sidenav folders (`navigate_next`)** such as Risk assessment
  sub-trees, related-party checklists, and most C-/D- fieldwork programs are
  not clicked through — only leaf items with direct `href`s (Materiality,
  Planning Checklist, Budget, Audit Risk Database) plus header tools.
- **Report download / Generate FAB** is visible in the assignment workspace
  but not covered by an end-to-end download assertion.
- **Role-scoped nav** — the UAT user used here exposes Dashboard / Client /
  Assignment at the shell level. Modules like Data Analytics or System
  Documents were not present in that sidenav and are not tested.
- **Fixture dependency** — workspace tests need
  `KNOWN_ASSIGNMENT_NAME` (default `Test AWMS_295 3.08.2026`) present on
  Search Assignment. If UAT data is purged, update `.env`.
- **Occasional post-login Independence redirect** was observed during
  exploration (`#/independence/fill-template`); the suite currently assumes
  a normal landing on `#/dashboard`.
- **No CI workflow** yet (`.github/workflows/` not added).
- Exploration helpers under `scripts/` are local-only and not part of the
  pytest suite.
