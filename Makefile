install:
	pip install -r requirements.txt
	python -m playwright install

format:
	black src/

test:
	pytest

test-headed:
	pytest --headed

test-tag:
	pytest -m $(TAG)

test-tag-headed:
	pytest -m $(TAG) --headed

report:
	allure generate reports/allure-results -o reports/allure-report --clean

report-serve:
	allure serve reports/allure-results

record:
	python -m playwright codegen "https://audit-uat.audtech.co.in/#/login"

clean:
	rm -rf reports/allure-results/* reports/allure-report/* screenshots/* logs/*.log .pytest_cache
