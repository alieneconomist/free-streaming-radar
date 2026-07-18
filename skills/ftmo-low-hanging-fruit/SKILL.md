---
name: ftmo-low-hanging-fruit
description: Scan a full MT5 symbol list for symbol-fit against any frozen strategy template and parameter set without changing EA code or inputs. Use when symbol substitution is the variable, the strategy should stay frozen, and the job is to rank a symbol universe and validate only the best fits with headless Strategy Tester runs.
---

# FTMO Optimization by Breadth

## Overview

Use this skill to find symbols that may already fit a frozen MT5 strategy template before any parameter optimization. Keep the EA code unchanged and keep the seed `.set` unchanged. The job is to identify the symbols that are most likely to work with the same setup, then confirm them with headless MT5 validation.

This applies to any existing strategy template under FTMO30, including Opening Range Breakout, Overnight Range Breakout, or another frozen EA.

Pair this skill with `shadow-testing` for the actual MT5 runs and `mt5-backtest-parity` when you need to compare against a stored report.

## Workflow

1. Anchor on one frozen seed.
   - Use the approved seed EA and the approved seed `.set`.
   - Keep symbol, timeframe, model, deposit, leverage, and date windows frozen for the first comparison pass.
   - Treat the seed as a symbol-fit reference, not a parameter-tuning target.

2. Build a symbol-fit shortlist from the full list.
   - Read the symbol universe from the provided CSV or broker symbol list.
   - Rank symbols by structural similarity to the seed:
     - same asset class first
     - same contract style and digits
     - similar spread and margin model
     - similar profit currency
     - similar market behavior bucket when known
   - For equity CFD seeds, check equities first, then indices, then other liquid CFDs.
   - For FX seeds, prefer the most liquid majors and the closest correlated crosses first.
   - For metals, commodities, or crypto seeds, stay within the same family before broadening out.

3. Use a two-stage screen.
   - Stage 1: cheap triage from symbol metadata only.
   - Stage 2: headless MT5 validation on the top shortlist with the exact same EA and `.set`.
   - Do not change parameters to force a symbol to pass.
   - Do not change code.

4. Validate the best fits.
   - Run MT5 Strategy Tester headlessly through `shadow-testing`.
   - Change only the symbol for the validation run.
   - Keep the same report window unless the strategy explicitly requires a symbol-specific date range.
   - Check net profit, profit factor, equity/balance drawdown, total trades, max consecutive losses, and tail-loss ratio.

5. Separate fit from robustness.
   - A symbol that looks good in one run is only a candidate.
   - Promote symbols that keep enough trades, acceptable drawdown, controlled loss clusters, strong PF, and reasonable tail ratio.
   - Mark low-trade outcomes as inconclusive, not as wins.

6. Extend only after the shortlist proves itself.
   - If the top few symbols look promising, expand to the next tier.
   - If nothing survives the first tier, stop and report that the seed may be symbol-specific.
   - Do not jump into hyper-optimization until the symbol-fit shortlist is known.

## Candidate Tiers

For a generic frozen strategy template, usually test in this order:

1. Same-family neighbors
   - nearest symbols in the same broker class
   - same underlying asset family
   - same digit / contract style

2. Liquid alternatives in the same market bucket
   - indices for equity-style seeds
   - major FX pairs and correlated crosses for FX-style seeds
   - related metals / commodities / crypto pairs for non-FX seeds

3. Broader liquid CFDs only if needed
   - `XAUUSD`
   - `EURUSD`
   - `GBPUSD`
   - `USDCHF`
   - `EURGBP`
   - `EURCHF`
   - `GBPCHF`
   - `AUDCAD`
   - `AUDNZD`

## Output Requirements

Produce these artifacts when practical:

- symbol-fit shortlist or ranked table
- headless MT5 report bundle for the shortlisted symbols
- summary of which symbols are close enough to keep testing
- summary of which symbols should be discarded early
- note explaining whether the seed appears symbol-agnostic or symbol-specific

## Guardrails

- Do not edit EA source code.
- Do not change strategy settings to manufacture a fit.
- Do not test every symbol with a huge sweep before a cheap metadata screen.
- Do not treat a single good symbol as proof that the whole list fits.
- Do not let multiple workers share the same terminal/profile/report path.
- Do not claim MT5 cannot run headlessly when a config-driven terminal path exists.
