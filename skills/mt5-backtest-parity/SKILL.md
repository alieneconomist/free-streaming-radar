---
name: mt5-backtest-parity
description: Reproduce and compare frozen MetaTrader 5 backtests for compiled EAs, .set files, sentiment/history CSVs, and stored Strategy Tester reports. Use when Codex needs to audit MT5 parity, rerun a report with the same inputs, extract report metrics, compare trade count and PnL/drawdown results, or determine whether a mismatch is caused by data quality, broker/profile drift, or a version mismatch rather than strategy logic.
---

# MT5 Backtest Parity

## Overview

Use this skill to reproduce a frozen MT5 Strategy Tester report as faithfully as the local machine allows, then compare the fresh run to the stored baseline. Keep EA logic and set parameters unchanged. If parity fails, diagnose the environment first: executable version, terminal/server profile, symbol naming, report window, and cached history quality.

When the run can be launched from disk, pair this with `shadow-testing` and run MT5 headlessly instead of relying on the interactive tester UI.

## Workflow

1. Inventory the local MT5 inputs.
   - Find the EA source and compiled binary.
   - Find the frozen `.set` file.
   - Find the sentiment/history CSV or other external data file the set references.
   - Find the stored Strategy Tester report and note whether it is HTML, PDF, or both.

2. Confirm the report baseline.
   - Read the report header for expert name, symbol, timeframe, date range, broker/server label, deposit, and history quality.
   - Extract the headline metrics: net profit, profit factor, maximal drawdown, and total trades.
   - If the report is a PDF, render or extract it before comparing numbers.

3. Re-run MT5 without changing strategy behavior.
   - Keep the EA logic frozen.
   - Keep the `.set` values frozen.
   - Make sure the CSV lands where MT5 expects it, usually `MQL5\Files`.
   - Use the same symbol, timeframe, deposit, and date range as the stored report.
   - Preserve the report name so the fresh output is easy to compare.

4. Compare the fresh report to the stored one.
   - Require exact trade-count match whenever possible.
   - Treat PnL, PF, and drawdown as parity metrics and compare them numerically.
   - Use a tight tolerance by default; if the user gives a specific threshold, follow that.
   - If the numbers differ, check build/version, broker/server profile, symbol naming, cached history quality, and report window before touching anything else.

5. Stop for data-quality gaps.
   - If the only credible cause is missing, stale, or broker-dependent history quality, report that explicitly and stop.
   - Do not "fix" parity by editing EA logic or parameter values.
   - Do not claim success until the stored baseline and fresh run are both verified against the same inputs.

## Useful Outputs

- Parity summary table with stored vs fresh metrics.
- Raw report bundle containing the original report and the fresh MT5 HTML.
- Short limitation note when parity is blocked by environment drift or data quality.
