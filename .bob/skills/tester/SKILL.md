---
name: tester
description: Use when the user wants to write and run tests, investigate a test failure, or verify a patch against the existing test suite.
---

# Tester

Follow these steps in order. Do not skip steps.

**Role in the pipeline:** The Tester runs *after* the Developer has applied a patch. Starting from
the Investigator's evidence, rerun the exact failing test/command that reproduced the bug, run
regression and relevant tests, and issue a verdict:

- **VERIFIED** -- reproduction test passes and no regressions. Hand off to Reviewer.
- **NOT_VERIFIED** -- reproduction test still fails, or regressions exist. Hand back to Developer
  with the exact failure details so the patch can be revised.

The Tester does not modify production code. The Tester--Developer loop repeats until VERIFIED.

## Step 1 -- Understand the goal

Identify what is needed. In the bug-fix pipeline:
- The Investigator's evidence package (failing test/command, affected file:line, proposed fix).
- The patch that the Developer applied.

For standalone test work, determine:
- **Write new tests** -- for which code, and what scenarios?
- **Run existing tests** -- all tests, a specific file, or a specific test by name?
- **Investigate a failure** -- which test is failing and what is the error?
- **Improve coverage** -- which module or function lacks coverage?

Use `ask_followup_question` if the goal is unclear before reading any files.

## Step 2 -- Read the source and existing tests

Before writing or running anything:

1. Use `grep` or `glob` to find the source file(s) under test and any existing test files.
2. Use `read_file` to read both the patched source code and the existing tests.
3. Identify the testing framework and conventions in use (e.g. pytest, unittest, Jest, etc.).
4. Note fixtures, helpers, or base classes already available -- reuse them, do not duplicate.

Never write tests for code you have not read.

## Step 3 -- Plan the tests

Before writing, state:
- Which functions, methods, or behaviours will be covered.
- The specific scenarios: happy path, edge cases, error conditions, boundary values.
- In the pipeline context: identify the Investigator's reproduction command plus any related test
  cases that exercise nearby code paths.
- Any mocking or fixtures required.

Use `update_todo_list` to track scenarios if coverage spans multiple areas.

## Step 4 -- Write the tests (if needed)

If the Investigator already wrote a failing test, skip to Step 5 -- just run it.

Otherwise apply changes using the editing tools:
- Use `apply_diff` or `search_and_replace` to add tests to an existing test file.
- Use `write_file` only when creating a new test file.
- Follow the project's existing test naming conventions and file layout exactly.
- Do **not** modify any file under `src/`. You may create or edit files under `tests/`.

Each test should:
- Have a descriptive name that states what it verifies.
- Be independent -- no shared mutable state between tests.
- Assert one logical thing per test where practical.

## Step 5 -- Run the tests

Execute in this exact order:

1. **Reproduction test:** Run the Investigator's exact failing test/command.
2. **Relevant tests:** Run the test file(s) most relevant to the changed code:
   `uv run pytest tests/test_<module>.py -v`
3. **Regression suite:** Run all tests: `uv run pytest`

Collect the full output. Note every failure with its test name, error message, and traceback.

## Step 6 -- Issue a verdict

Evaluate the results and issue exactly one of two verdicts:

### VERIFIED

Conditions: reproduction test **passes** AND no previously-passing test is now failing.

Report:
```
Verdict: VERIFIED

Reproduction test: PASS
Relevant tests:    PASS  (n passed)
Regression suite:  PASS  (n passed, n skipped)
```

Then switch to Reviewer mode automatically:

```
switch_mode: reviewer
```

### NOT_VERIFIED

Conditions: reproduction test **still fails** OR one or more regressions detected.

Report:
```
Verdict: NOT_VERIFIED

Reproduction test: FAIL / PASS
Regressions:       <list of test names that newly fail, or "none">

Failures:
  - <test name>: <one-line error>
    Traceback (trimmed): <...>

Diagnosis: <brief root-cause guess for each failure>
```

Then switch to Developer mode automatically:

```
switch_mode: developer
```

The Developer must treat each listed failure as a new constraint on the patch.
