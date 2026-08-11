"""
Locator strategies for the Dashboard / shell (header + sidenav).
Ordered fallbacks — BasePage.resolve() tries each in order.
"""

LOGOUT_MENU_ITEM = [
    lambda p: p.locator("span.logout"),
    lambda p: p.get_by_text("Logout", exact=True),
    lambda p: p.get_by_role("menuitem", name="Logout"),
]

DECLARATION_MENU_ITEM = [
    lambda p: p.get_by_text("Declaration", exact=True),
    lambda p: p.get_by_role("menuitem", name="Declaration"),
]

DASHBOARD_HEADING = [
    lambda p: p.locator("div.link.currentPage", has_text="Dashboard"),
    lambda p: p.locator("div.crumb", has_text="Dashboard"),
    lambda p: p.get_by_text("Recent Assignments", exact=True),
]

SIDENAV_DASHBOARD = [
    lambda p: p.locator("a.sidenav-item[href='#/dashboard']"),
    lambda p: p.locator("a.sidenav-item", has_text="Dashboard"),
    lambda p: p.get_by_role("link", name="Dashboard"),
]

SIDENAV_CLIENT = [
    lambda p: p.locator("a.sidenav-item").filter(has=p.locator("mat-icon", has_text="supervisor_account")),
    lambda p: p.locator("a.sidenav-item").filter(has_text="Client").first,
]

SIDENAV_CREATE_CLIENT = [
    lambda p: p.locator("a.sidenav-item[href='#/client/addclientform']"),
    lambda p: p.locator("a.sidenav-item", has_text="Create Client"),
]

SIDENAV_SEARCH_CLIENT = [
    lambda p: p.locator("a.sidenav-item[href='#/client']"),
    lambda p: p.locator("a.sidenav-item", has_text="Search Client"),
]

SIDENAV_ASSIGNMENT = [
    lambda p: p.locator("a.sidenav-item").filter(has=p.locator("mat-icon", has_text="import_contacts")),
    lambda p: p.locator("a.sidenav-item").filter(has_text="Assignment").first,
]

SIDENAV_CREATE_ASSIGNMENT = [
    lambda p: p.locator("a.sidenav-item[href='#/assignment/create']"),
    lambda p: p.locator("a.sidenav-item", has_text="Create Assignment"),
]

SIDENAV_SEARCH_ASSIGNMENT = [
    lambda p: p.locator("a.sidenav-item[href='#/assignment']"),
    lambda p: p.locator("a.sidenav-item", has_text="Search Assignment"),
]

SIDENAV_ARCHIVED_ASSIGNMENT = [
    lambda p: p.locator("a.sidenav-item[href='#/assignment/archived']"),
    lambda p: p.locator("a.sidenav-item", has_text="Archived Assignment"),
]

RECENT_ASSIGNMENTS_SECTION = [
    lambda p: p.get_by_text("Recent Assignments", exact=True),
    lambda p: p.locator("text=Recent Assignments"),
]

SIDENAV_TOGGLE = [
    lambda p: p.get_by_role("button", name="menu"),
    lambda p: p.locator("button").filter(has=p.locator("mat-icon", has_text="menu")),
    lambda p: p.locator("button.mdc-icon-button").filter(has_text="menu"),
]

CREATE_NEW_BUTTON = [
    lambda p: p.get_by_role("button", name="CREATE NEW"),
    lambda p: p.locator("button", has_text="CREATE NEW"),
]
