---
name: mt5-bridge
description: Headless MT5 Strategy Tester bridge package for preparing job manifests, launching isolated terminal runs, parsing HTML reports, reconciling expected Python-side metrics against MT5 results, and verifying report identity. Use when Codex needs to stage or run MT5 backtests or OOS checks from frozen EAs and .set files, bundle artifacts, name the execution gap, or confirm a report matches a requested symbol, timeframe, and date range.
---

# MT5 Bridge

Use this skill when the task is to move between Python-side orchestration and MT5 Strategy Tester output without changing strategy logic.

Treat the bridge as a shippable package with four parts:
- CLI entrypoint
- MT5 launcher and job staging
- MT5 report parser and verifier
- sample manifest / example job

Prefer the packaged workflow before inventing one-off scripts.

## Core workflow

1. Normalize the job inputs.
   - Expert name or EA path.
   - Frozen `.set` file.
   - Symbol, period, start date, end date.
   - Optional server, login, report name, and external files.

2. Stage one isolated job.
   - Keep one terminal root per job whenever possible.
   - Keep one config file, one report base, and one artifact folder per job.
   - Copy the frozen EA and inputs into the terminal tree only when needed.

3. Launch MT5 headlessly.
   - Prefer the bundled bridge package when it exists.
   - Use the CLI entrypoint or a prepared tester `.ini` / manifest-driven launcher.
   - Do not change EA logic or inputs to make the run "fit".
   - If MT5 must be opened interactively, document the blocker first.

4. Reconcile the gap.
   - Compare expected Python-side metrics to MT5 report metrics.
   - Name the likely mismatch class: execution blocked, sparse signal, edge collapse, logic drift, risk mismatch, or generic performance drift.
   - Use the gap result to decide whether to patch the manifest, patch the environment, or reject the strategy.

5. Verify the report.
   - Parse the HTML report back into metrics.
   - Confirm expert, symbol, timeframe, from/to dates, and build/server label.
   - Treat mismatches as contamination unless the user explicitly allows a looser comparison.

6. Persist the artifact bundle.
   - Keep the launch config.
   - Keep the copied report bundle.
   - Keep a machine-readable summary for downstream analysis.
   - Keep the manifest or CLI inputs that produced the run.

## When to use

- Prepare or run an MT5 backtest from frozen inputs.
- Verify that a Strategy Tester report matches the intended job.
- Compare a Python simulation claim against MT5 reality.
- Parse MT5 HTML reports into JSON or CSV.
- Batch several MT5 jobs with isolated folders.
- Build a reusable bridge between Python orchestration and MT5 execution.
- Use a saved bridge package instead of ad hoc launch glue.

## Practical rules

- Prefer `python -m mt5_bridge prepare|run|parse|verify|reconcile` when the package is present.
- Keep each job self-identifying with a unique `job_id` and `report_name`.
- Avoid shared tester state between concurrent jobs.
- Treat the report as the artifact of record.
- If the run fails, record the exact blocker, the attempted fix, and what still works.

## Outputs

- Launch `.ini`
- Job manifest snapshot
- Copied report bundle
- Parsed JSON metrics
- Verification result
- Gap classification

## Minimal commands

```powershell
python -m mt5_bridge prepare examples\orb_tsla_sample.json --output work\mt5_bridge\prepared.json
python -m mt5_bridge verify examples\orb_tsla_sample.json outputs\orb_raw_mt5_reports\ORB_TSLA3_target_rvol140_or20.htm
python -m mt5_bridge reconcile expected.json actual_report.htm
python -m mt5_bridge run examples\orb_tsla_sample.json --output work\mt5_bridge\last_run.json
```
