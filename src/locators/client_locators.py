"""
Locator strategies for Client Create + Search screens.
"""

# ---- Search Client (#/client) ----

SEARCH_CLIENT_NAME = [
    lambda p: p.locator('input[formcontrolname="organizationname"]'),
    lambda p: p.get_by_label("Client Name"),
]

SEARCH_CLIENT_EMAIL = [
    lambda p: p.locator('input[formcontrolname="email"]'),
    lambda p: p.get_by_label("Email"),
]

SEARCH_CLIENT_CONTACT = [
    lambda p: p.locator('input[formcontrolname="mobilenumber"]'),
    lambda p: p.get_by_label("Contact no."),
]

SEARCH_STATUS = [
    lambda p: p.locator('mat-select[formcontrolname="state"]'),
    lambda p: p.get_by_label("Status"),
]

SEARCH_BUTTON = [
    lambda p: p.get_by_role("button", name="search"),
    lambda p: p.locator("button").filter(has=p.locator("mat-icon", has_text="search")),
]

CLIENT_TABLE_ROWS = [
    lambda p: p.locator("table tbody tr, mat-row, .mat-mdc-row"),
]

CLIENT_TABLE = [
    lambda p: p.get_by_role("table"),
    lambda p: p.locator("table, mat-table"),
]

ADD_CLIENT_ICON = [
    lambda p: p.locator("button").filter(has=p.locator("mat-icon", has_text="add")),
    lambda p: p.get_by_role("button", name="add"),
]

# ---- Create Client (#/client/addclientform) ----

CLIENT_NAME = [
    lambda p: p.locator('input[formcontrolname="client"]'),
    lambda p: p.get_by_label("Client Name"),
]

REGISTRATION_NO = [
    lambda p: p.locator('input[formcontrolname="registrationNo"]'),
    lambda p: p.get_by_label("Registration No."),
]

FY_ENDS_ON = [
    lambda p: p.locator('input[formcontrolname="Period"]'),
    lambda p: p.get_by_label("Financial Year Ends On"),
]

ORG_TYPE = [
    lambda p: p.locator('mat-select[formcontrolname="orgTypeId"]'),
    lambda p: p.get_by_label("Organization Type"),
]

INDUSTRY_TYPE = [
    lambda p: p.locator('mat-select[formcontrolname="IndustryType"]'),
    lambda p: p.get_by_label("Industry Type"),
]

CURRENCY = [
    lambda p: p.locator('mat-select[formcontrolname="currencyId"]'),
    lambda p: p.get_by_label("Currency"),
]

NEXT_BUTTON = [
    lambda p: p.get_by_role("button", name="NEXT"),
    lambda p: p.locator("button", has_text="NEXT"),
]

STEP_BASIC_INFO = [
    lambda p: p.get_by_text("Basic Info", exact=True),
    lambda p: p.locator("text=Basic Info"),
]

PAGE_TITLE_CREATE = [
    lambda p: p.get_by_text("Create", exact=True),
    lambda p: p.locator("text=Create"),
]

VALIDATION_ERROR = [
    lambda p: p.locator("mat-error"),
    lambda p: p.get_by_role("alert"),
    lambda p: p.locator(".mat-mdc-form-field-error"),
]
