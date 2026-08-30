# Debug Pipeline Optimization Plan

## Top-Level Overview

The current `.bob/` configuration defines a four-stage bug-fix pipeline
(Investigator → Developer → Tester → Reviewer) via `custom_modes.yaml`, four skill
files, and three rules files. A full audit revealed seven categories of issues:
conflicting permissions, stale project rules, redundant prose, inconsistent
terminology, a broken test setup, and unclear handoff contracts.

The goal is a single coherent, self-consistent pipeline where every file says
exactly what it means, the rules match the actual code, the test setup is
executable, and every mode/skill/rules file contributes unique information.

**Non-goals:** no new features, no changes to the Python source code, no
restructuring of the pipeline stages themselves.

---

## Sub-Tasks

---

### Sub-task 1 — Fix pytest dependency so the pipeline's test commands actually work

**Status:** [x] done

**Intent**  
Every skill (`developer`, `tester`) and both rules files reference `uv run pytest`,
but `pytest` is not declared anywhere in `pyproject.toml`. The reproduction test
(`tests/test_validation.py`) imports `pytest` and will fail to import. This must
be fixed before anything else, as it blocks the entire Tester stage.

**Expected Outcomes**
- `pytest` is declared under `[dependency-groups.dev]` in `pyproject.toml`.
- `uv run pytest` resolves and runs without import errors.
- `tests/test_validation.py` passes.
- `tests/test_main.py` is replaced with a minimal but real pytest test (or removed)
  so it does not silently produce zero results.

**Todo List**
1. Add `[dependency-groups.dev]` section to `pyproject.toml` with `pytest`.
2. Run `uv sync --group dev` to verify lock file updates.
3. Replace the `print("Hi from the test")` in `tests/test_main.py` with at least
   one real pytest test function (e.g. a smoke test that imports `MusicParser`).
4. Run `uv run pytest` and confirm all tests in `tests/test_validation.py` pass
   and `tests/test_main.py` is discovered with at least one passing test.

**Relevant Context**
- `pyproject.toml:10-18` — dependencies section; add `[dependency-groups.dev]` after it.
- `tests/test_main.py:1` — contains only `print("Hi from the test")`.
- `tests/test_validation.py` — real tests that import `pytest`; currently broken.
- `.bob/rules-plan/AGENTS.md:6` — acknowledges the gap but gives wrong placement
  hint ("add it under `[project.optional-dependencies]`"); fix this hint too.

---

### Sub-task 2 — Tighten Tester permissions and clarify the "no production code edits" constraint

**Status:** [x] done

**Intent**  
The Tester `roleDefinition` says "You never modify production code" but its `groups`
list includes `edit`, which grants unrestricted file modification. The skill already
says the same restriction, but the permission model offers no enforcement. The
simplest fix is to keep `edit` (needed to write test files) but add an explicit
callout in the `customInstructions` and skill so the constraint is unambiguous.

**Expected Outcomes**
- `custom_modes.yaml` Tester `customInstructions` explicitly states which files may
  be edited (test files only) and which must not be touched (source under `src/`).
- `tester/SKILL.md` Step 4 and Step 6 both clarify "do not modify files under `src/`".
- The Tester skill description is updated so "improve test coverage for existing code"
  reads as "write and run tests for existing code" (no ambiguity about editing source).

**Todo List**
1. In `custom_modes.yaml` Tester `customInstructions`, add: "You may only edit files
   under `tests/`. Never modify any file under `src/`."
2. In `tester/SKILL.md` Step 4, change "Do not modify production code" to
   "Do not modify any file under `src/`. You may create or edit files under `tests/`."
3. Update the frontmatter `description` in `tester/SKILL.md` from "improve test
   coverage for existing code" to "write and run tests for existing code".

**Relevant Context**
- `.bob/custom_modes.yaml:61-88` — Tester mode definition.
- `.bob/skills/tester/SKILL.md:3` — frontmatter description.
- `.bob/skills/tester/SKILL.md:64` — "Do not modify production code."

---

### Sub-task 3 — Define a standard evidence package format and propagate it across all four files

**Status:** [x] done

**Intent**  
The "evidence package" is the handoff artifact from Investigator to Developer. Its
definition differs across files:
- `github-issue-triage/SKILL.md` Step 7 lists: root cause (file + line), failing
  test/command, proposed fix snippet.
- `reviewer/SKILL.md` Step 1 lists: root cause *statement*, reproduction command
  *and output*, proposed fix.

The two lists differ in detail and naming. The Developer depends on this contract,
so it must be consistent in every file that references it.

**Expected Outcomes**
- A single canonical evidence package definition is established in
  `github-issue-triage/SKILL.md` Step 7 with labeled fields.
- `developer/SKILL.md` Step 1 uses identical field names.
- `reviewer/SKILL.md` Step 1 uses identical field names.
- `custom_modes.yaml` Investigator `roleDefinition` and `whenToUse` use identical
  field names.

**Canonical format to use:**
```
Evidence Package:
- Root cause: <file>:<line> — <one sentence explanation>
- Reproduction command: <exact command>
- Reproduction output: <trimmed output showing the failure>
- Proposed fix: <code snippet or description>
```

**Todo List**
1. Add the canonical format block to `github-issue-triage/SKILL.md` Step 7 under
   "Present the evidence package for the Developer".
2. Update `developer/SKILL.md` Step 1 (First entry section) to use the same field
   names.
3. Update `reviewer/SKILL.md` Step 1 to use the same field names (currently says
   "root cause statement, reproduction command and output, proposed fix").
4. Update `custom_modes.yaml` Investigator `roleDefinition` inline reference from
   "root cause (file + line), failing test/command, and proposed fix" to match the
   canonical field names.

**Relevant Context**
- `.bob/skills/github-issue-triage/SKILL.md:137-152` — Step 7 handoff.
- `.bob/skills/developer/SKILL.md:21-26` — Step 1, first-entry block.
- `.bob/skills/reviewer/SKILL.md:22-25` — Step 1 evidence items list.
- `.bob/custom_modes.yaml:7-9` — Investigator `roleDefinition`.

---

### Sub-task 4 — Trim redundant prose in custom_modes.yaml

**Status:** [x] done

**Intent**  
Each mode in `custom_modes.yaml` has three fields that say the same thing:
`roleDefinition`, `whenToUse`, and `description`. The `customInstructions` then
paraphrases the skill steps again. This duplication makes it harder to keep files
in sync and adds no value to the pipeline.

Specifically:
- `description` should be a one-line tagline (different from `whenToUse`).
- `whenToUse` should say *when* to invoke, not *what* the agent does.
- `roleDefinition` may be kept as-is (it is the agent's identity).
- `customInstructions` should say "activate skill X and follow its steps" — not
  re-list the steps inline.

**Expected Outcomes**
- `description` for all four modes is a single concise tagline (≤ 15 words).
- `whenToUse` for all four modes answers "when should I switch to this mode?" only.
- `customInstructions` for all four modes says only "Always activate the X skill.
  Follow its steps exactly." No inline step summaries.
- Total line count of `custom_modes.yaml` is reduced.

**Todo List**
1. Rewrite the `customInstructions` for all four modes to remove inline step
   paraphrasing. Each `customInstructions` should be 1-2 sentences.
2. Review `whenToUse` for all four modes; remove any content that merely repeats
   `roleDefinition`.
3. Optionally shorten `description` if it overlaps with `whenToUse`.

**Relevant Context**
- `.bob/custom_modes.yaml:1-115` — all four mode definitions.

---

### Sub-task 5 — Update the three rules files to match actual project state

**Status:** [x] done

**Intent**  
The three rules files (`rules-agent`, `rules-ask`, `rules-plan`) were written at
project setup and have drifted from reality. Specific issues:
1. `rules-plan/AGENTS.md` says "add pytest under `[dependency-groups]` or
   `[project.optional-dependencies]`" — neither section existed before Sub-task 1;
   after Sub-task 1 the correct section is `[dependency-groups.dev]`.
2. `rules-ask/AGENTS.md` says "`__init__.py:main()` is a stub" but gives no
   guidance on the intended architecture. This leaves Ask/Plan agents without
   direction.
3. `rules-agent/AGENTS.md` references `writeCsv()` AttributeError as a known issue
   but no test exists for it; this should be flagged explicitly.
4. All three files are silent on the pytest test infrastructure added in Sub-task 1.

**Expected Outcomes**
- `rules-plan/AGENTS.md` references `[dependency-groups.dev]` as the correct
  location for test dependencies and notes pytest is now declared there.
- `rules-ask/AGENTS.md` documents the intended architecture decision for
  `__init__.py:main()` (either "wire to `helper.MusicParser`" or "leave as stub —
  use `main.py` directly for dev").
- `rules-agent/AGENTS.md` adds a note: "No test exists for the `writeCsv()`
  AttributeError; add one before shipping any CSV-related feature."
- All three files note the test suite is now runnable via `uv run pytest --group dev`
  (or the correct `uv` incantation after Sub-task 1 is confirmed).

**Todo List**
1. Edit `rules-plan/AGENTS.md`: update the pytest note to reference the new
   `[dependency-groups.dev]` section.
2. Edit `rules-ask/AGENTS.md`: add one bullet that states the architectural decision
   for `__init__.py:main()`.
3. Edit `rules-agent/AGENTS.md`: add the missing test coverage note for
   `writeCsv()` AttributeError, and update the "uv run" line to confirm tests work.
4. After Sub-task 1 is complete, verify the exact `uv run` command and standardize
   it across all three rules files and both skill files.

**Relevant Context**
- `.bob/rules-plan/AGENTS.md:6` — stale pytest guidance.
- `.bob/rules-ask/AGENTS.md:3-4` — `__init__.py:main()` stub description.
- `.bob/rules-agent/AGENTS.md:4` — `writeCsv()` AttributeError note.
- `src/music_parser/__init__.py` — current stub code.
- `src/music_parser/helper.py:40-46` — `writeCsv()` implementation.

---

### Sub-task 6 — Clarify mcp and subagent group permissions in custom_modes.yaml

**Status:** [x] done

**Intent**  
The Investigator and Developer both list `mcp` in their `groups`, but neither skill
file references any MCP tool or explains why this permission is needed. The Reviewer
lists `subagent` but is explicitly forbidden from editing files — and a subagent
could theoretically edit files. These permissions should either be justified with a
comment or removed.

**Expected Outcomes**
- If `mcp` is needed for GitHub API calls (Investigator) or tool use (Developer),
  a comment in `custom_modes.yaml` says so.
- If `mcp` is not needed, it is removed from Investigator and Developer `groups`.
- A note in the Reviewer section explains why `subagent` is listed despite the
  "never edit" constraint.
- The final permission sets for all four modes are intentional and documented.

**Todo List**
1. Research whether `mcp` is required for GitHub REST API calls via
   `execute_command` (it probably is not — those are shell commands, not MCP calls).
2. If `mcp` is not needed for Investigator/Developer, remove it from those groups.
3. Add a short inline comment to the Reviewer `groups` explaining why `subagent` is
   kept (e.g. "to delegate read-only exploration tasks").
4. Verify the Tester does not need `mcp` (it doesn't have it — confirm this is
   intentional).

**Relevant Context**
- `.bob/custom_modes.yaml:21-29` — Investigator groups (includes `mcp`).
- `.bob/custom_modes.yaml:51-59` — Developer groups (includes `mcp`).
- `.bob/custom_modes.yaml:110-114` — Reviewer groups (includes `subagent`).

---

## Execution Order

Sub-tasks have the following dependencies:

```
Sub-task 1 (pytest setup) → Sub-task 5 (update rules) must come after
Sub-task 3 (evidence format) → Sub-task 4 (trim prose) must come after
Sub-tasks 2, 6 are independent
```

Recommended order: **1 → 2 → 3 → 4 → 5 → 6**
