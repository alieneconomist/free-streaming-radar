---
name: mt5-oos-test
description: Run MT5 out-of-sample tests with a post-IS date range that is comparable to the in-sample window, then evaluate net profit, profit factor, drawdown, and trade count. Use when choosing or correcting an OOS range, rerunning a frozen compiled EA with the same set file and market data, or reviewing OOS performance for ranking or elimination.
---

# MT5 OOS Test

## Overview

Use this skill when the OOS slice needs to stay meaningful relative to the in-sample run. A 30-day OOS window is usually too short unless the in-sample window is similarly short.

When the OOS job can be driven from a saved config or `.ini`, use `shadow-testing` to run it headlessly and keep the tester UI out of the way.

## Workflow

1. Identify the in-sample end date and choose an OOS start date immediately after it.
2. Prefer an OOS duration that is comparable to the in-sample window, or at least the same order of magnitude.
3. Run MT5 Strategy Tester with the frozen EA, the frozen `.set` file, and the same broker/data profile.
4. Extract OOS net profit, profit factor, max drawdown, and total trades.
5. Treat zero-trade or very-low-trade runs as evaluation-limited, not as normal ranked outcomes.

## Evaluation Rules

- Do not shrink the OOS window just to get a quick answer.
- Do not change EA logic, symbol settings, or parameters to make the test fit.
- If the OOS window is too short to be comparable, widen it before judging performance.
- Call out when flat results are driven by no trades, spread filters, session filters, or missing data.

## Output

Report the OOS date range, the four core metrics, and a short judgment on whether the slice is informative enough to compare across strategy sets.
