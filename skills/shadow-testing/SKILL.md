---
name: shadow-testing
description: Run MT5 Strategy Tester headlessly from prepared config or ini files and frozen inputs. Use when launching no-popup backtests, optimizations, or OOS runs, preserving compiled EAs and .set files, or writing audit-ready report bundles without interactive tester popups.
---

# Shadow Testing

## Overview

Use this skill to run MT5 tests from a prepared launch config instead of the interactive tester UI. Keep the EA, `.set`, symbol, timeframe, and date range frozen, and favor hidden or background execution when the run can be driven entirely from disk.

MT5 Strategy Tester can be driven headlessly from a prepared config or `.ini`. Do not treat popups as required.

## Workflow

1. Collect the frozen inputs.
   - Find the compiled EA, matching `.set` file, and any required CSV or history files.
   - Note the baseline report name, symbol, timeframe, broker/server label, and date range.

2. Prepare a headless launch.
   - Use the MT5 portable terminal when possible.
   - Drive the tester with a saved config or `.ini` so no popups are needed.
   - Keep all strategy inputs frozen.
   - If another agent says MT5 cannot run headless, treat that as a workflow mistake, not a platform limit.

3. Run the test without changing behavior.
   - Do not edit EA logic.
   - Do not change parameters to make the run fit.
   - If the run needs extra history or tick data, fetch it before judging results.

4. Collect the outputs.
   - Save the generated HTML, PDF, or XML report.
   - Save the launch config or `.ini` used for the run.
   - Record MT5 build, symbol, timeframe, date range, and any data-quality notes.

## Guardrails

- Prefer no-popup, disk-driven execution whenever the test can be launched that way.
- Preserve original inputs and write reports into a separate output folder.
- Treat the tester report as the artifact of record.
- If parity or OOS evaluation is the goal, pair this skill with `mt5-backtest-parity` or `mt5-oos-test`.

## Outputs

- MT5 report bundle
- launch config or `.ini`
- short audit note with build, symbol, timeframe, date range, and result summary
