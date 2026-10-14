# Static Code Analysis Issues — Campus Shuttle Timetable & Fleet Tracker

The line numbers below refer to the original, unmodified `shuttle_system.py` submitted for analysis.

| Issue | Type / Severity | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Route R3 accessed after deletion | Bug — Medium | 55, 58 | `main()` removes R3 and then calls `average_load("R3")`, causing `KeyError`. | Keep R3 available until its data has been displayed; handle unknown routes explicitly. |
| Invalid passenger counts | Data validation bug — Medium | 48–50; 11–13 | Negative counts and the string `"full"` are added as if they were valid passenger counts. | Validate route IDs and require a non-negative integer; use valid sample counts in `main()`. |
| Mutable default argument | Bug / maintainability — Medium | 11 | `logs=[]` is shared by calls that omit the argument, so log entries can leak across calls. | Use `logs=None` and create a new list inside the function. |
| Broad exception silently suppressed | Error handling — Medium | 26–30 | `except: pass` hides unrelated errors, including invalid data and division-by-zero problems. Bandit reports this as B110 and Flake8 reports E722. | Avoid catching everything; validate inputs and handle empty trip lists explicitly. |
| Empty route average | Bug — Medium | 19–21 | An empty `trips` list causes division by zero when the average is requested. | Return `0.0` for a route with no recorded trips, and document that behavior. |
| Pseudo-random driver choice flagged | Bandit B311 — Low | 33–35 | Bandit warns that `random.choice()` is unsuitable for cryptographic purposes. Driver assignment is not security-sensitive, so this is a low-priority warning in this context. | Use `secrets.choice()` to satisfy the scanner and avoid the B311 finding. Cryptographic randomness is not otherwise required for this use case. |
| File opened without context manager or encoding | Code quality — Low | 37–43 | Manual `open()` / `close()` calls can leave files open if an error occurs, and text encoding is unspecified. | Use `Path.open()` with a `with` block and `encoding="utf-8"`; write JSON using `json.dump()`. |
| Naming and missing docstrings | Style / maintainability — Low | 1, 11, 16, 19, 23, 33, 37, 45 | The module and functions lack docstrings, and `assignDriver` does not follow snake_case. | Add useful docstrings and rename the function to `assign_driver`. |
| Flake8 spacing and line length | Style — Low | 11, 13, 16, 19, 23, 33, 37, 45, 60 | Several definitions need PEP 8 blank-line spacing and one line exceeds 79 characters. | Apply PEP 8 spacing and wrap long lines. |
| Unused driver assignment parameter | Code quality — Low | 33 | `route_id` is accepted by `assignDriver()` but not used to validate a route. | Check that the route exists before assigning a driver. |

## Verification plan

After applying the fixes, rerun Pylint, Bandit, and Flake8. Compare their reports against the saved `reports_before` results. A finding should be marked resolved only after it no longer appears in the corresponding after-fix report.
