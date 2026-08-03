# Agent Operating Guide

You are extending this framework against the **live** AWM UAT app at the
URL in `.env` (`BASE_URL`). You have real browser access this framework's
original author (an LLM in a sandboxed chat) did not — use it. Explore
before you generate code; don't guess locators.

## Ground rules

1. **Never hardcode values.** Read from `config.settings`, not literals.
   Add new fields to `Settings` (settings.py) and `.env.example` — never
   put real credentials in `.env.example` or in source.
2. **Every page object inherits `BasePage`.** Use `safe_click`,
   `safe_fill`, `safe_select`, `safe_upload`, `expect_visible`,
   `expect_text`, `expect_url`. Don't call `page.click()` etc. directly
   in a page object — that bypasses logging, screenshots, and retries.
3. **Locators live in `src/locators/<feature>_locators.py`**, as ordered
   fallback lists (see `login_locators.py`). Page objects call
   `self.resolve(loc.SOME_ELEMENT, "description")` — never inline a raw
   `page.locator(...)` string directly in a page object method body.
   Prefer `get_by_role`, `get_by_label`, `get_by_placeholder`, or
   `data-testid` as the primary strategy; CSS/XPath only as a fallback.
4. **One feature = one locators file + one page object + one test
   module** under `src/tests/<feature>_test/test_<feature>.py`, matching
   the `login_test/` example.
5. **Register every new page object** in `PageManager` inside
   `src/tests/conftest.py`.
6. **Tag every test** with at least one marker (`smoke`, `regression`,
   `positive`, `negative`) and wrap with `@allure.feature` /
   `@allure.story` / `@allure.severity`, matching `test_login.py`.
7. **Document assumptions inline** as a comment where you made one (e.g.
   "assuming Save always redirects to list view — confirm") rather than
   silently guessing.

## Exploration workflow (do this per feature area)

1. Log in (`make test-tag TAG=smoke` should already get you a passing
   login, or run `make record` to open Playwright codegen against the
   live app and click around manually to capture selectors).
2. Navigate to the feature/module in the running app. Inventory what's
   there: forms, tables, buttons, dropdowns, filters, modals, file
   upload/download, pagination, validation messages.
3. For each interactive element you'll need, capture 2-3 locator
   strategies (role/label/placeholder first, a CSS fallback second) and
   put them in that feature's `_locators.py` file.
4. Build the page object, then the test module: positive path, at least
   one negative/validation path, and a boundary case if the field has
   obvious limits (e.g. required field empty, file type/size limits on
   uploads).
5. Run the tests. If something fails:
   - Check `logs/automation.log` and the screenshot in `screenshots/`
     for the failure.
   - If it's a locator problem, fix the locator file (promote whichever
     fallback actually matched, per the log, or add a new one) — don't
     just add more retries.
   - If it's a timing problem, `@self_heal()` already retries — but
     consider whether an explicit `expect_visible()` wait before the
     action would fix it more cleanly than relying on retries.
   - Re-run until green, or if genuinely blocked (e.g. a backend bug,
     missing test data), mark the test `@pytest.mark.skip(reason="...")`
     with a clear reason and note it under "Known limitations" in
     README.md — don't leave it silently failing.
6. Generate the report (`make report-serve`) and sanity-check it shows
   what you expect before moving to the next feature.

## Suggested feature order

Mirrors the original assignment's priority list — critical path first:

1. Login / logout / session (logout is already stubbed in
   `dashboard_page.py` — finish it first, other tests may need it)
2. Dashboard navigation (confirm menu structure — this seeds locators
   for everything else)
3. Client management (search, add client)
4. Assignment management (create, search assignment)
5. Core audit workflow screens: materiality, risk assessment, trial
   balance, planning checklist
6. Review/sign-off flows: manager review points, sign-off, related-party
   checklist
7. Reporting: download report, templates, system documents
8. Everything else (data analytics, audit journal, budget, client
   queries, my profile, change password)

The old reference project (if you have it alongside this one) had page
objects for most of these already — useful for understanding what fields
and flows existed previously, but **verify every locator against the
live app first**; the assignment brief notes the app has been updated
since that code was written, so treat the old code as a hint, not ground
truth.

## Deliverables checklist (from the original assignment)

- [x] Framework skeleton, POM architecture, self-healing base, logging,
      screenshot-on-failure, Allure reporting, `.env` handling — done.
- [x] Page object coverage for login, dashboard, client, assignment,
      assignment workspace (materiality / checklist / TB / sign-off menu /
      header tools), profile — see README coverage table.
- [x] Positive / negative / boundary / validation tests per covered module
- [x] All tests green on last full run (39 passed, 2026-08-03)
- [x] `logs/`, `screenshots/`, `reports/allure-results/` populated from a
      real run (HTML Allure report blocked without Java — see README)
- [x] README "Known limitations" section updated to reflect actual state
- [x] Git commits per feature
