# Testing Guide — Project SaBai Backend

This guide explains how tests are organized in this repository, how the pieces fit together, and practical advice for writing and running tests.

**Important Files & Directories**

- `api/tests/`
  - `dummies/`: payload definitions (dicts) for different domains (patients, visits, consults, medication, orders, vitals, ...). Payload names follow the numeric pattern: `post_<domain>_dummy_1`, `post_<domain>_dummy_2`, etc.
  - `factories.py`: functions like `patient_payloads()`, `medication_payloads()` that collect payloads from `dummies/` and (optionally) batch ORM creators like `create_patients_from_dummies()`.
  - `fixtures.py`: pytest fixtures built from factories (e.g. `patient`, `visit`, `consult`) and batch fixtures (e.g. `all_dummy_patients`). These produce pre-existing DB state tests often need.
  - `custom_api_client.py`: `CustomAPIClient` wrapper around DRF `APIClient` with helpers and standardized response handling.
  - `conftest.py`: test-level fixtures and setup (registers assert-rewrite for helper modules and exposes `api_client`, `test_user`).
  - `test_*.py`: test modules covering endpoints and behaviors.
- `sabaibiometrics/custom_exception_handler.py`: normalizes DRF error shapes (e.g. 4xx responses become `{"error": "..."}` and 5xx include `error_id`) so `CustomAPIClient` can assert predictable shapes.
- `pytest.ini` (repo root): project-level pytest config. It can include `addopts = -vv --showlocals --reuse-db` so failures print full locals and verbose diffs.

**How They Interlink**

- Tests import payloads from `api.tests.factories` (which aggregates `api/tests/dummies`).
- Fixtures in `api/tests/fixtures.py` create DB objects or call APIs and are imported by `api/tests/conftest.py` so they're available globally.
- `api_client` fixture (from `conftest.py`) returns a `CustomAPIClient` instance; tests use it for authenticated requests.
- `CustomAPIClient` expects server error responses to contain "error" in json.
- `pytest.ini` configures the default test-run behavior (verbosity, showing locals), which improves failure output for debugging.

**Writing Tests — Quick Checklist**

- Use `@pytest.mark.django_db` for tests that use the DB.
- Use `api_client` and `test_user` fixtures for authenticated requests.
- Pull a payload and store it in a local variable to avoid repeated calls:
- Arrange: prepare payload or fixtures.
- Act: call the endpoint: `api_client.post(reverse("medication:medications_list"), payload, headers={"doctor": test_user.email})`.
- Assert: check `response.status_code` and `response.data` shape. For errors, assert `"error" in response.data`.
- Keep tests focused: one behavior per test.

**Step-by-step: Writing a New Test**

1. Create or open a file under `api/tests/` named `test_<feature>.py`.
2. Add required imports:

```py
import pytest
from rest_framework.reverse import reverse
from api.tests.factories import <domain>_payloads
```

3. If the test touches the DB, add the marker:

```py
@pytest.mark.django_db
```

4. Create a local `payload` variable at the top of the test function to avoid repeating `*_payloads()[0]`:

```py
payload = <domain>_payloads()[0]
```

5. Use the `api_client` fixture and call the endpoint:

```py
response = api_client.post(
  reverse("<app>:<route_name>"),
  payload,
  headers={"doctor": test_user.email},
)
```

6. Assert the result (status and response body):

```py
assert response.status_code == 201
assert response.data["field"] == payload["field"]
```

7. Add separate tests for edge cases (missing headers, invalid data, permissions).
8. Run the single test (or file) locally and iterate until passing:

```powershell
pipenv run pytest api/tests/test_<feature>.py::test_name -q
```

9. When stable, run the whole file and/or the full suite:

```powershell
pipenv run pytest api/tests/test_<feature>.py
pipenv run pytest
```

10. Commit with a clear message and include what the test covers in the PR description.

Quick tips:

- Keep tests small and focused.
- Prefer fixtures for repeated setup rather than duplicating creation logic.
- Use `--pdb` and `--maxfail=1` for debugging failing tests.

**Example Test Pattern**

- Structure:
  - Arrange: create or reference `payload` and fixtures.
  - Act: perform API call via `api_client`.
  - Assert: status + response body fields.
    (See the detailed Step-by-step section for a complete example.)

**Best Practices for This Repo**

- Use payload lists and a local `payload` variable in tests: `payload = patient_payloads()[0]`.
- Prefer fixtures for setup where tests need existing DB state (use `patient`, `visit`, `consult` fixtures).
- Avoid asserting raw numeric primary keys unless the test explicitly controls them — prefer checking fields.
- For error tests, assert the normalized error shape: `assert "error" in response.data`.
- Make tests idempotent: rely on pytest-django DB isolation and `--reuse-db` in CI as needed.

**Running & Debugging Tests**

- Run a single test file:

```
pipenv run pytest api/tests/test_medication.py
```

- Run a single test function:

```
pipenv run pytest api/tests/test_medication.py::test_medication_post
```

- Use verbose failure output (repo `pytest.ini` includes `-vv --showlocals` by default). To ensure full verbose output, run `pytest` without `-q`.
- Helpful flags:
  - `-k <expr>` to filter tests
  - `--maxfail=1` to stop after first failure
  - `--pdb` to drop into pdb on failure

**Extending Tests — Adding Payloads, Factories & Fixtures**

- Add payloads in `api/tests/dummies/<domain>.py` using the numeric pattern `post_<domain>_dummy_1`.
- Export them via `api/tests/dummies/__init__.py` so `factories.py` can collect them.
- Update `api/tests/factories.py` to expose `*_payloads()` accessors.
- Add new fixtures to `api/tests/fixtures.py` and import them in `api/tests/conftest.py` if you need them available globally.
- For repeated ORM creation, add batch creators (e.g. `create_medications_from_dummies()`) in `factories.py`.

**Common Pitfalls & Fixes**

- Assertion output truncated: run `pytest` (not `-q`) — repo `pytest.ini` sets `-vv --showlocals` by default to show locals and verbose diffs.
- Tests fail because server error shape changed: ensure `sabaibiometrics/custom_exception_handler.py` normalizes errors to `{"error": "..."}` for 4xx and includes an `error_id` for 5xx.
- Legacy dummy names in tests: convert to `*_payloads()[0]` and use a local `payload` variable.
- Fixtures not registered: ensure `api/tests/conftest.py` imports fixtures from `api/tests/fixtures.py`.

**Pre-commit Checklist for New Tests**

- Payload: `payload = domain_payloads()[0]` used where appropriate.
- Fixture: `api_client`, `test_user` or domain fixture used for setup.
- Marker: `@pytest.mark.django_db` present if DB used.
- Assertions: status code and response shape asserted; error assertions check `"error"`.
- Run tests locally and make sure they pass: `pipenv run pytest <path>`.

---

If you want, I can:

- Convert the remaining test files to the `payload` variable pattern automatically.
- Create a PR with example tests or run the full test suite and report failures (with full outputs).

Where should I save the guide next (another filename), or should I create a short README snippet linking to this file?
