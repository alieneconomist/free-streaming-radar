---
name: mt5-isolated-launcher
description: Launch headless MT5 Strategy Tester jobs in isolated terminal folders with unique configs, report paths, and job IDs. Use when Codex needs to prevent shared-state drift between concurrent MT5 runs, diagnose a run that later appears to use the wrong strategy or .set, or keep multiple tester jobs separate while preserving frozen EA logic and inputs.
---

# Mt5 Isolated Launcher

## Core rule

One job equals one terminal instance, one config file, one report path, and one output folder.
Do not rely on the GUI; drive MT5 from the prepared tester config or `.ini`.

## Use this skill for

- Parallel MT5 backtests or optimizations.
- Headless MT5 runs that must not show tester popups.
- Jobs that drift onto the wrong expert, symbol, timeframe, or .set.
- Any batch where shared tester state could contaminate results.

## Launcher pattern

1. Copy the portable MT5 tree for the job.
2. Put the frozen EA, frozen `.set`, and any CSV inputs into the job-local files path.
3. Write a unique tester `.ini` or config for that job.
4. Use a unique report name and unique output folder.
5. Start only that job.
6. Verify the final HTML report header, not just the running process.

## Verification checks

- Expert name matches the intended job.
- Symbol and timeframe match the job.
- From/to dates match the job.
- Report filename matches the job.
- MT5 build/server label matches expectations.
- Output folder contains only the files for that job.

If any check fails, treat the run as contaminated and rerun it in a fresh isolated folder.

## Failure signals

- Wrong strategy or wrong set appears later in the run.
- A report watcher picks up a stale HTML file.
- Two jobs share the same tester cache or output path.
- The terminal restarts and falls back to a default profile.

These are isolation problems, not evidence that MT5 cannot run headlessly.

## Worker prompt

Use this wording when handing the job to another agent:

> Launch MT5 headlessly from a job-local portable terminal and tester config. Keep each run isolated in its own folder. Do not use shared report paths or shared config paths. Verify the report header after the run and stop if the expert, set, symbol, or date range does not match the job.

## Related skills

- `shadow-testing` for headless MT5 execution from prepared configs.
- `mt5-bridge` for job manifests, report parsing, and gap reconciliation.
