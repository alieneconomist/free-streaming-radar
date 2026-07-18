---
name: male-linear-regression
description: Analyze frozen MT5 strategy runs with linear regression to identify key parameters driving performance, rank the top needle movers, and guide optimization for MALE-style result tables or similar backtest matrices.
---

# MALE Linear Regression

## Purpose

Use this skill to attribute MT5 strategy performance to the parameters that matter most.
Treat MT5 backtest outputs as ground truth and use regression as an explanation tool, not proof of edge.

## Workflow

1. Keep the EA logic frozen.
2. Collect a clean matrix of runs with one row per test.
3. Include only variables that changed across runs.
4. Use MT5-backed outputs as targets, typically:
   - net profit
   - profit factor
   - drawdown
   - trade count
   - tail-risk measures such as largest loss / average loss
5. Standardize inputs before fitting so coefficient sizes are comparable.
6. Fit a linear model first.
7. Check collinearity, sparse coverage, and obvious outliers before trusting ranks.
8. Rank variables by standardized impact and stability across folds or repeated runs.
9. Call out the top needle movers first.
10. Only then decide whether deeper parameter optimization is worth the cost.

## Interpretation Rules

- Prefer simple, transparent models first.
- Treat low sample size or highly correlated variables as tentative.
- Do not claim a parameter is causal unless MT5 validation supports it.
- If the regression and MT5 report disagree, trust MT5 and name the gap.
- Focus on reducing loss clusters and drawdown while keeping profit factor high and tail risk low.

## Output

When using this skill, report:
- the candidate variables
- the regression target(s)
- the top ranked parameters
- the direction of effect
- any collinearity or instability warnings
- the next MT5 validation step

## Related MT5 Skills

Use mt5-backtest-parity to verify baseline reproduction.
Use mt5-bridge or shadow-testing for headless MT5 runs.
Use tmo-strategy-optimizer when you move from attribution into parameter search.
