---
name: mt5-market-fallback-retry
description: Handle invalid-price pending order failures in any MT5 EA by retrying immediately as a market order, recalculating take profit from the actual fill price, and logging the fallback path without coupling to a specific strategy.
---

# MT5 Market Fallback Retry

## Core Use

Use this skill when an MT5 EA places a pending order, receives an invalid-price failure, and should retry immediately as a market order.

Keep the pattern strategy-agnostic:

- Do not assume a specific entry model.
- Do not assume a specific exit model.
- Do not assume a specific signal source.
- Treat the retry logic as an execution wrapper around any EA.

## Required Flow

1. Build the original pending order.
2. Send the pending order.
3. If the platform reports invalid price, retry immediately as a market order.
4. Recompute TP from the actual fill price before sending the market order.
5. Reuse the same SL, side, and volume unless the broker requires a safe adjustment.
6. Log the pending failure, the fallback decision, and the market outcome.

## Take Profit Rule

When falling back to a market order:

- Recalculate TP from the market fill price, not the original pending price.
- Preserve the original RR logic or target-selection logic.
- Keep TP far enough from the fill to avoid near-zero-distance exits.

## Logging Rule

Log these events distinctly:

- original pending request
- invalid-price failure
- fallback market retry
- recalculated market TP
- final market order outcome

## Integration Rules

- Keep the fallback function reusable from any EA.
- Avoid shared state tied to one strategy’s signal engine.
- Pass in the order side, SL, TP builder, and lot size as inputs.
- Return success or failure to the caller so the EA can continue its own workflow.
- Prefer a small helper that can be wrapped around existing order submission code.
