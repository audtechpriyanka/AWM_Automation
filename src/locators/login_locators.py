"""
Locator strategies for the Login page, expressed as ordered lists of
callables (primary first, fallbacks after). BasePage.resolve() tries
each in order and logs when a fallback had to be used.

When the app changes and a primary selector breaks:
  1. Confirm which fallback picked up the slack (check logs/automation.log
     for "Locator fallback used for ...").
  2. Promote that fallback to position 0 here.
  3. Add a fresh fallback guess after it if useful.
Do NOT delete history — leave the old primary as a fallback for one
release cycle in case the change gets reverted.
"""

USERNAME_FIELD = [
    lambda p: p.locator('input[name="email"]'),
    lambda p: p.get_by_placeholder("Email"),
    lambda p: p.locator('input[type="email"]'),
]

PASSWORD_FIELD = [
    lambda p: p.locator('input[name="password"]'),
    lambda p: p.get_by_placeholder("Password"),
    lambda p: p.locator('input[type="password"]'),
]

SIGN_IN_BUTTON = [
    lambda p: p.get_by_role("button", name="SIGN IN"),
    lambda p: p.get_by_role("button", name="Sign In"),
    lambda p: p.locator('button[type="submit"]'),
]

ERROR_MESSAGE = [
    lambda p: p.get_by_role("alert"),
    lambda p: p.locator(".cdk-overlay-container"),
    lambda p: p.get_by_text("Invalid Credentials"),
]

LOGO = [
    lambda p: p.locator(".logo"),
    lambda p: p.get_by_role("img", name="logo"),
]

FORGOT_PASSWORD_LINK = [
    lambda p: p.get_by_text("Forgot Password"),
    lambda p: p.get_by_role("link", name="Forgot Password"),
]
