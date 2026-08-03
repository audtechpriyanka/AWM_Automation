"""
Self-healing utilities used by BasePage.

Two mechanisms, deliberately kept simple and inspectable:

1. `resolve_locator(page, strategies, description)`
   Takes an ordered list of locator-building callables (primary selector
   first, fallbacks after). Tries each in order, returns the first one
   that resolves to a visible element. Logs which strategy worked so the
   working one can be promoted back to primary in the page object later.

2. `@self_heal(retries=...)`
   Decorator for page-object action methods. On failure, logs a
   diagnostic snapshot (URL, page title, a screenshot) and retries with
   backoff before finally re-raising. This does NOT invent new locators —
   it buys robustness against timing/flakiness. Actual locator repair
   (updating a selector because the app changed) is a deliberate action
   the agent takes in the page object source, not something hidden here.
"""
import functools
import time
from typing import Callable, List

from playwright.sync_api import Locator, Page, TimeoutError as PWTimeoutError

from config.settings import settings
from utilities.logger import get_logger
from utilities.screenshots import capture_screenshot

logger = get_logger("self_healing")


def resolve_locator(page: Page, strategies: List[Callable[[Page], Locator]], description: str) -> Locator:
    """
    Try each locator-building strategy in order; return the first that
    is attached and visible within a short timeout. Raises the last
    error if none succeed.
    """
    last_error = None
    for i, strategy in enumerate(strategies):
        try:
            locator = strategy(page)
            locator.first.wait_for(state="visible", timeout=3000)
            if i > 0:
                logger.warning(
                    "Locator fallback used for '%s' — strategy #%d succeeded, "
                    "primary strategy may need repair.",
                    description, i + 1,
                )
            return locator
        except Exception as e:  # noqa: BLE001 - intentionally broad, we're probing
            last_error = e
            continue

    logger.error("All %d locator strategies failed for '%s'", len(strategies), description)
    capture_screenshot(page, f"locator_failure_{description}")
    raise last_error or RuntimeError(f"No locator strategy resolved for '{description}'")


def self_heal(retries: int = None, backoff_ms: int = None):
    """
    Decorator for BasePage/page-object methods. Retries the wrapped
    action on Playwright timeout/errors, capturing a screenshot and
    diagnostic log on each failure.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            max_retries = retries if retries is not None else settings.max_action_retries
            wait_ms = backoff_ms if backoff_ms is not None else settings.retry_backoff_ms
            attempt = 0
            while True:
                try:
                    return func(self, *args, **kwargs)
                except (PWTimeoutError, Exception) as e:  # noqa: BLE001
                    attempt += 1
                    page = getattr(self, "page", None)
                    action_name = func.__name__
                    if page is not None:
                        capture_screenshot(page, f"{action_name}_attempt{attempt}")
                        logger.error(
                            "Action '%s' failed on attempt %d/%d | url=%s | error=%s",
                            action_name, attempt, max_retries + 1, page.url, e,
                        )
                    else:
                        logger.error(
                            "Action '%s' failed on attempt %d/%d | error=%s",
                            action_name, attempt, max_retries + 1, e,
                        )
                    if attempt > max_retries:
                        raise
                    time.sleep(wait_ms / 1000)
        return wrapper
    return decorator
