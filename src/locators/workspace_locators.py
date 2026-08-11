"""
Locators for the AWM assignment workspace shell (header + section sidenav).
Deep screens (materiality, checklist, etc.) are opened via these nav entries.
"""

SECTION_ENGAGEMENT = [
    lambda p: p.locator("a.sidenav-item").filter(has_text="A-Engagement Management"),
]

SECTION_RISK_PLANNING = [
    lambda p: p.locator("a.sidenav-item").filter(has_text="B-Risk Assessment & Planning"),
]

SECTION_FIELDWORK = [
    lambda p: p.locator("a.sidenav-item").filter(has_text="C-Risk Response & Field Work"),
]

SECTION_REPORTING = [
    lambda p: p.locator("a.sidenav-item").filter(has_text="D-Reporting & Completion"),
]

NAV_MATERIALITY = [
    lambda p: p.locator("a.sidenav-item").filter(has_text="Materiality"),
    lambda p: p.get_by_text("B2.0 - Materiality"),
]

NAV_PLANNING_CHECKLIST = [
    lambda p: p.get_by_text("B12.0 - Planning Checklist"),
    lambda p: p.locator("a.sidenav-item").filter(has_text="Planning Checklist"),
    # Retained only for older UAT builds; live UAT exposes Planning Checklist as B12.0.
    lambda p: p.get_by_text("B11.0 - Planning Checklist"),
]

NAV_BUDGET = [
    lambda p: p.locator("a.sidenav-item").filter(has_text="B12.0 - Budget"),
    lambda p: p.locator("a.sidenav-item").filter(has_text="Budget").first,
]

NAV_RISK_DATABASE = [
    lambda p: p.locator("a.sidenav-item").filter(has_text="Audit Risk Database"),
    lambda p: p.get_by_text("B8.0 - Audit Risk Database"),
]

NAV_RELATED_PARTY = [
    lambda p: p.locator("a.sidenav-item").filter(has_text="related party"),
    lambda p: p.get_by_text("C17.0 - Directors and related party transactions"),
]

HEADER_TRIAL_BALANCE = [
    lambda p: p.locator("button.headerMenu", has_text="Trial Balance"),
    lambda p: p.get_by_role("button", name="Trial Balance"),
]

HEADER_TEMPLATES = [
    lambda p: p.locator("button.headerMenu", has_text="Templates"),
    lambda p: p.get_by_role("button", name="Templates"),
]

HEADER_CLIENT_QUERIES = [
    lambda p: p.locator("button.headerMenu", has_text="Client Queries"),
    lambda p: p.get_by_role("button", name="Client Queries"),
]

HEADER_AUDIT_JOURNAL = [
    lambda p: p.locator("button.headerMenu", has_text="Audit Journal"),
    lambda p: p.get_by_role("button", name="Audit Journal"),
]

HEADER_SAMPLING = [
    lambda p: p.locator("button.headerMenu", has_text="Sampling"),
    lambda p: p.get_by_role("button", name="Sampling"),
]

HEADER_SIGN_OFF = [
    lambda p: p.locator("button.headerMenu", has_text="Sign-Off"),
    lambda p: p.get_by_role("button", name="Sign-Off"),
]

HEADER_HOME = [
    lambda p: p.locator("button.headerMenu", has_text="home"),
    lambda p: p.get_by_role("button", name="home"),
]

OVERVIEW_TAB = [
    lambda p: p.get_by_role("tab", name="Overview"),
    lambda p: p.locator(".mdc-tab", has_text="Overview"),
]

SAVE_BUTTON = [
    lambda p: p.get_by_role("button", name="SAVE"),
    lambda p: p.get_by_role("button", name="Save"),
    lambda p: p.locator("button", has_text="SAVE"),
]

DOWNLOAD_BUTTON = [
    lambda p: p.get_by_role("button", name="Download"),
    lambda p: p.locator("button", has_text="Download"),
]
