"""
Locator strategies for Assignment Create + Search screens.
"""

# ---- Search Assignment (#/assignment) ----

SEARCH_CLIENT = [
    lambda p: p.locator('input[formcontrolname="clientId"]'),
    lambda p: p.get_by_label("Select Client"),
]

SEARCH_STATUS = [
    lambda p: p.locator('mat-select[formcontrolname="assignmentStatusId"]'),
    lambda p: p.get_by_label("Select Assignment Status"),
]

SEARCH_TYPE = [
    lambda p: p.locator('mat-select[formcontrolname="assignmentType"]'),
    lambda p: p.get_by_label("Select Assignment Type"),
]

SEARCH_BUTTON = [
    lambda p: p.get_by_role("button", name="search"),
    lambda p: p.locator("button").filter(has=p.locator("mat-icon", has_text="search")),
]

ASSIGNMENT_TABLE_ROWS = [
    lambda p: p.locator("table tbody tr, mat-row, .mat-mdc-row"),
]

ASSIGNMENT_NAME_LINKS = [
    lambda p: p.locator("table a, mat-cell a, .mat-mdc-cell a"),
]

# ---- Create Assignment (#/assignment/create) ----

ASSIGNMENT_NAME = [
    lambda p: p.locator('input[formcontrolname="assignment"]'),
    lambda p: p.get_by_label("Assignment Name"),
]

CLIENT = [
    lambda p: p.locator('input[formcontrolname="clientId"]'),
    lambda p: p.get_by_label("Select Client"),
]

ASSIGNMENT_TYPE = [
    lambda p: p.locator('mat-select[formcontrolname="assignmentType"]'),
    lambda p: p.get_by_label("Select Assignment Type"),
]

ASSIGNEE = [
    lambda p: p.locator('mat-select[formcontrolname="userIds"]'),
    lambda p: p.get_by_label("Select Assignee"),
]

START_DATE = [
    lambda p: p.locator('input[formcontrolname="startDate"]'),
    lambda p: p.get_by_label("Financial Year Start Date"),
]

END_DATE = [
    lambda p: p.locator('input[formcontrolname="endDate"]'),
    lambda p: p.get_by_label("Financial Year End Date"),
]

AMOUNT_FORMAT = [
    lambda p: p.locator('mat-select[formcontrolname="amountFormat"]'),
    lambda p: p.get_by_label("Amount Format"),
]

CREATE_BUTTON = [
    lambda p: p.get_by_role("button", name="CREATE"),
    lambda p: p.locator('button[type="submit"]', has_text="CREATE"),
]

OPTION = [
    lambda p: p.locator("mat-option"),
]

MAT_OPTION_BY_TEXT = None  # resolved dynamically in page object

VALIDATION_ERROR = [
    lambda p: p.locator("mat-error"),
    lambda p: p.get_by_role("alert"),
    lambda p: p.locator(".mat-mdc-form-field-error"),
]

PAGE_HEADING = [
    lambda p: p.get_by_text("Create", exact=True),
    lambda p: p.locator("text=Assignment"),
]
