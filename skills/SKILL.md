---
name: detailed-logs
description: Add deterministic signal-troubleshooting logs to any MT5 EA. Use when an EA needs step-by-step validation output for trade signals, rejection reasons, sizing failures, order placement outcomes, or other cases where a trade should have happened but did not.
---

# Detailed Logs

## Core Use

Use this skill when instrumenting any MT5 EA so each signal can explain its own decision path in the journal.

Apply it when the user wants:

- one compact report per signal or bar
- explicit reject reasons at every gate
- order send success/failure logging
- sizing and margin troubleshooting
- trade-signal debugging that survives live runs and tester runs
- integration-safe logs that do not depend on a specific strategy engine

## Logging Contract

For every signal, emit logs in a fixed order:

1. Start of evaluation
2. Data sufficiency checks
3. Spread and session gates
4. Duplicate-bar / cooldown checks
5. Sentiment or bias checks
6. Zone discovery checks
7. Candle-pattern or rejection checks
8. Position-cap and pending-order checks
9. Sizing checks
10. Order submission result

## Required Reject Reasons

Use explicit reason text when a trade does not happen:

- insufficient bars
- spread too wide
- duplicate signal already processed
- sentiment unavailable
- sentiment threshold not decisive
- no qualifying zone
- sentiment/zone mismatch
- no valid rejection candle
- same-direction position cap reached
- invalid risk distance
- zero volume after sizing
- runtime gate blocked order placement
- order send failed

## Message Style

- Prefix each signal with one stable tag.
- Include symbol, timeframe, bar time, and direction where useful.
- Keep messages short and deterministic.
- Emit one clear rejection line per failed gate.
- Emit one success line when an order is actually sent.
- Include computed values only when they help troubleshoot the failure.

## Porting Checklist

When adding the logging pattern to an EA:

1. Wrap each early return with a log line.
2. Return a reason string from helper functions that can fail.
3. Log calculated values for sentiment, zone selection, and sizing.
4. Log both the broker retcode and the platform error on order failure.
5. Preserve the log order across all signals so issues are easy to compare.
6. Keep the logging helpers side-effect free so they can be reused by any strategy module.
