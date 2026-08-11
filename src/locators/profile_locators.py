"""Locator strategies for profile navigation in the header user menu."""

USER_MENU_BUTTON = [
    lambda p: p.locator("button.user-button"),
    lambda p: p.locator("button").filter(has=p.locator("mat-icon", has_text="keyboard_arrow_down")),
    lambda p: p.get_by_role("button").filter(has_text="keyboard_arrow_down"),
]

PROFILE_MENU_ITEM = [
    lambda p: p.get_by_text("Profile", exact=True),
    lambda p: p.get_by_role("menuitem", name="Profile"),
]

CHANGE_PASSWORD_MENU_ITEM = [
    lambda p: p.get_by_text("Change Password", exact=True),
    lambda p: p.get_by_role("menuitem", name="Change Password"),
]

PROFILE_IMAGE_INPUT = [
    lambda p: p.locator('input[type="file"][accept*="image"]'),
    lambda p: p.locator('input[type="file"]'),
]

PROFILE_IMAGE_CROP_BUTTON = [
    lambda p: p.get_by_role("button", name="Crop"),
    lambda p: p.locator("button", has_text="Crop"),
]

PROFILE_IMAGE_PREVIEW = [
    lambda p: p.locator("img.profilepicture"),
]

REMOVE_PHOTO_BUTTON = [
    lambda p: p.get_by_role("button", name="Remove Photo"),
    lambda p: p.locator("button", has_text="Remove Photo"),
]

PROFILE_UPDATE_BUTTON = [
    lambda p: p.get_by_role("button", name="UPDATE"),
    lambda p: p.locator("button", has_text="UPDATE"),
]
