---
name: github-issue-triage
description: Use when the user wants to triage, investigate, or resolve a GitHub issue — fetches open issues from the repo, lets the user pick one, reproduces/analyzes it in the codebase, and posts a solution comment back to the GitHub issue.
metadata:
  argument-hint: "[owner/repo]"
---

# GitHub Issue Triage

Follow these steps in order. Do not skip steps.

**Role in the pipeline:** The Investigator runs *before* any patch is applied. The goal of this
skill is to confirm the bug exists in the current (unpatched) code, reproduce it with a failing
test or command, identify the root cause, and hand off a concrete evidence package to the Developer.
The Investigator does **not** apply fixes.

## Step 1 -- Identify the repository

If the user has not provided a `owner/repo` slug:
- Check the current workspace for clues: look for a `git remote` by running `execute_command` with
  `git remote get-url origin` and parse the owner/repo from the URL.
- If that fails, ask the user: "Which GitHub repo should I look at? (e.g. `owner/repo`)"

Store the result as `REPO`.

Also check whether a `GITHUB_TOKEN` environment variable is available. If not, inform the user:
> "No GITHUB_TOKEN found. I can still fetch public issues, but posting a comment will require a
> token. Set GITHUB_TOKEN in your environment and restart, or provide it now."

## Step 2 -- Fetch and display open issues

Run the fetch script:
```
execute_command: python <skill-dir>/fetch-issues.py <REPO>
```

Where `<skill-dir>` is the directory containing this `SKILL.md` file (typically
`~/.bob/skills/github-issue-triage/`).

Display the list to the user, then ask:
> "Which issue number would you like to investigate?"

## Step 3 -- Load the full issue

Run:
```
execute_command: python <skill-dir>/fetch-issues.py <REPO> <ISSUE_NUMBER>
```

Read and summarize the issue: title, description, reproduction steps (if any), and any relevant
comments.

## Step 4 -- Investigate and reproduce

Using the codebase tools (`grep`, `read_file`, `FindSymbol`, etc.):

1. Identify which files/functions are relevant to the reported problem.
2. Trace the code path that would trigger the issue.
3. **Reproduce the bug on unpatched code:**
   - Run existing tests with `execute_command` (e.g. `uv run pytest`). Identify any that already
     fail due to this bug.
   - If no existing test covers the scenario, write a minimal failing test or command that
     demonstrates the bug and run it. Confirm it fails for the right reason.
   - Save the exact command and output -- this becomes the reproduction evidence.
4. Identify the root cause. Quote the specific file and line(s) where the bug lives.

Do **not** fix the code at this step. The failing test/command must stay failing so the Developer
and Tester can verify before and after the patch.

## Step 5 -- Formulate a solution

Based on your investigation:
- Clearly state the root cause (one sentence).
- Propose a concrete fix (code change, config change, documentation update, etc.) with a code
  snippet.
- Note any edge cases or caveats.
- List the exact failing test/command the Developer and Tester should use to verify the fix.

Do **not** apply the fix to the code at this stage -- this step is analysis only.

## Step 6 -- Post the analysis as a GitHub issue comment

Compose a comment in this format:

```
## Analysis

**Root cause:** <one sentence>

**Affected code:** `<file>:<line>` -- <brief explanation>

**Reproduction (unpatched):** <confirmed / not confirmed / partially confirmed>
Command: `<exact command>`
Output:
```
<trimmed output showing the failure>
```

## Proposed Fix

<description of the fix, with code snippet>

## Verification steps

After applying the fix, run:
```
<exact command(s) the Tester should run>
```
Expected result: <all tests pass / specific output>

## Notes

<any caveats, alternative approaches, or follow-up questions>

---
*Analysis by Bob (AI assistant)*
```

Then post it using `execute_command`:
```
execute_command:
  $env:GITHUB_TOKEN = "<token>"   # only if not already in environment
  $body = @{ body = "<escaped comment text>" } | ConvertTo-Json
  Invoke-RestMethod -Method Post `
    -Uri "https://api.github.com/repos/<REPO>/issues/<ISSUE_NUMBER>/comments" `
    -Headers @{
      Authorization = "Bearer $env:GITHUB_TOKEN"
      Accept = "application/vnd.github+json"
      "X-GitHub-Api-Version" = "2022-11-28"
    } `
    -Body $body `
    -ContentType "application/json"
```

If `GITHUB_TOKEN` is not set, show the user the comment text and instruct them to post it manually.

## Step 7 -- Confirm and hand off

Tell the user:
- The URL of the issue where the comment was posted (from the API response `html_url`), or
- That the comment text is ready to paste manually if no token was available.

Present the evidence package for the Developer using this exact structure:

```
Evidence Package:
- Root cause: <file>:<line> — <one sentence explanation>
- Reproduction command: <exact command>
- Reproduction output: <trimmed output showing the failure>
- Proposed fix: <code snippet or description>
```

Then switch to Developer mode automatically:

```
switch_mode: developer
```
