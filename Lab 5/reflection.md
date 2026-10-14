# Lab 5 Reflection — Static Code Analysis

*Draft note: The uploaded handout lists the learning outcomes but does not include the four reflection questions. These answers are organized around those learning outcomes. If your instructor provided separate questions, update the headings to match them before submission.*

## 1. What is static code analysis, and what did the three tools check?

Static code analysis examines source code without running the program. In this lab, Pylint checked code quality and maintainability, including docstrings, naming, unused arguments, and problematic coding patterns. Bandit highlighted potentially unsafe patterns, while Flake8 checked Python style and formatting rules such as blank lines and line length.

## 2. What issues did you find in the original program?

The original program used a mutable default argument (`logs=[]`), silently ignored exceptions with `except: pass`, and could divide by zero when a route had no trips. It also accepted invalid passenger values such as negative counts and the string `"full"`. The program removed route R3 and then tried to calculate its average, which caused a `KeyError`. The tools also identified style and maintainability problems, including missing docstrings, a function name that did not follow snake_case, and file operations without a context manager or explicit encoding.

## 3. How did you fix the issues, and what were the results?

I replaced the mutable default with `None` and initialized a new list when needed. I added route and passenger-count validation, handled empty trip lists explicitly, removed the broad exception suppression, and changed the order of operations so R3 is read before it is removed. I also added docstrings, used snake_case naming, improved JSON file handling with a context manager and explicit encoding, and adjusted formatting. In the final run shown in my report, Pylint improved from 6.25/10 to 10.00/10, and Bandit reported no issues identified. The final Flake8 report should also be checked and retained as evidence that style violations were resolved.

## 4. How does static analysis help, and what are its limitations?

Static analysis helps detect possible defects and inconsistent style early, before code is delivered or tested manually. Using several tools is useful because each focuses on a different area: general code quality, security-related patterns, or style. However, a clean report does not prove that a program is completely correct; tools may miss runtime or domain-specific problems and may also report warnings that need context. I still need to run the program with representative inputs and review the tool findings before deciding how to fix them.
