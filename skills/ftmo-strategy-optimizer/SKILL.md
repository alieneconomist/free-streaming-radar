---
name: ftmo-strategy-optimizer
description: Optimize MT5 strategy parameters for FTMO challenge readiness using frozen EA logic, headless Strategy Tester runs, in-sample and out-of-sample validation, and linear-regression parameter attribution. Use when symbols are frozen and parameters are the variable, whether the template is Opening Range Breakout, Overnight Range Breakout, or another existing FTMO30 EA.
---

# FTMO Optimization by Depth

## Overview

Use this skill to turn a frozen MT5 strategy template into an FTMO-ready candidate through parameter-only optimization. Keep EA source and compiled logic unchanged unless the user explicitly consents to code changes.

This applies to any existing strategy template under FTMO30, including Opening Range Breakout, Overnight Range Breakout, or another frozen EA.

Pair this skill with `shadow-testing`, `mt5-backtest-parity`, and `mt5-oos-test` when available.

## Workflow

1. Inventory the strategy package.
   - Locate the EA source and compiled `.ex5`.
   - Locate baseline `.set` files.
   - Locate stored MT5 Strategy Tester reports, usually PDF/HTML/XML.
   - Identify symbol, timeframe, broker/server, deposit, leverage, model, and date range from the report header.

2. Establish the baseline.
   - Run the frozen baseline through MT5 Strategy Tester headlessly from a prepared `.ini` or tester config.
   - Do not use MetaTrader5 Python as a substitute for Strategy Tester results.
   - Compare fresh metrics against the stored report: net profit, profit factor, drawdown, trades, largest loss, average loss, and max consecutive losses.
   - If strict parity fails but the user accepts close performance parity, document the drift and continue only as a relative optimization study in one consistent environment.

3. Install or stage MALE5 when requested.
   - Clone or copy `MegaJoctan/MALE5` into a task workspace.
   - Install a copy under the isolated MT5 terminal's `MQL5\\Include\\MALE5` path.
   - Do not inject MALE5 into the EA source unless the user approves code changes.
   - For parameter attribution, a transparent external OLS/ridge-style regression over MT5 report metrics is acceptable when EA code must remain frozen.

4. Build a parameter-only sweep.
   - Start with a narrow needle-mover pass before hyper-optimizing.
   - Change one high-leverage variable at a time to identify the biggest drivers of net profit, profit factor, drawdown, loss clusters, and tail risk.
   - Use the regression/correlation output from prior runs to rank likely movers before expanding the sweep.
   - Only broaden into denser hyper-optimization after the top few drivers are known.
   - Generate `.set` variants from the frozen baseline or the existing profitable set.
   - Vary only exposed input parameters.
   - Keep magic number, symbol, timeframe, model, deposit, leverage, and date windows controlled unless the test explicitly varies them.
   - Prioritize parameters likely to affect FTMO risk quality: entry strictness, stop distance, target/partial behavior, breakeven, trailing stop, max holding, daily loss cap, account loss cap, and trade limits.

5. Run tests with isolated shadow testing.
   - Use one portable MT5 folder per batch or worker.
   - Use one job-local config and one unique report name per run.
   - Verify report headers after each run; discard contaminated reports where expert, symbol, timeframe, or date range do not match.
   - Clear oversized tester logs between runs if disk pressure appears.

6. Score for FTMO readiness.
   - Reward high profit factor and sufficient trade count.
   - Penalize high equity/balance drawdown.
   - Penalize high max consecutive losses.
   - Penalize tail risk, measured as `abs(largest loss trade) / abs(average loss trade)`.
   - Flag low-trade runs instead of promoting them, even if PF is huge.

7. Run OOS validation.
   - Use a comparable post-IS out-of-sample range, not a tiny convenience slice.
   - Promote only candidates that keep enough trades, acceptable drawdown, controlled loss clusters, strong PF, and reasonable tail ratio out of sample.
   - If OOS has too few trades, mark the candidate inconclusive rather than FTMO-ready.

8. Attribute parameter effects.
   - Build a table with full parameter values plus MT5 metrics for every valid run.
   - Run linear regression or correlation-style attribution against targets such as score, profit factor, equity drawdown %, tail-loss ratio, and max consecutive loss count.
   - Interpret coefficients cautiously when the sample is small or parameters are collinear.
   - Report both direction and trade-off, e.g. a parameter may raise PF while worsening tail-loss ratio.
   - Use the attribution pass to decide the next needle-mover probe before moving into a wider sweep.

## Output Requirements

Produce these artifacts when practical:

- IS sweep CSV and markdown summary.
- OOS validation CSV and markdown summary.
- Linear regression attribution CSV.
- Raw MT5 report bundle or paths to generated HTML/XML reports.
- Recommendation stating whether any candidate is FTMO-ready, inconclusive, or rejected.
- Limitation notes for parity drift, low trade count, data quality, or disk/log failures.

## Guardrails

- Do not edit EA source code without explicit consent.
- Do not silently change strategy logic to improve results.
- Do not promote a low-trade OOS result as robust.
- Do not let multiple workers share the same terminal/profile/report path.
- Do not claim MT5 cannot run headlessly when a config-driven terminal path exists.
