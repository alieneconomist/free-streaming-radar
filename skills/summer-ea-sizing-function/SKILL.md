---
name: summer-ea-sizing-function
description: Reuse the Summer EA position sizing system in any MT5 EA, including fixed lot, fixed ratio, dollar risk, percentage sizing, prior-profit inclusion, equity floor, user volume caps, and margin guards. Use when porting or recreating sizing logic without tying it to a specific entry, exit, or strategy model.
---

# Summer EA Sizing Function

## Core Use

Use this skill when implementing or reusing the Summer EA sizing model in any MT5 EA.

Apply it when the task needs one or more of these behaviors:

- Fixed lot sizing
- Fixed ratio progression sizing
- Dollar-risk sizing
- Percent-of-available-balance sizing
- Prior-trade-profit inclusion
- Minimum equity floor protection
- Optional user volume cap
- Optional minimum margin level resizing

## Sizing Modes

Use the same four sizing modes:

1. `Fixed_Lot`
   - Return the configured lot size directly.

2. `Dynamic`
   - Use the fixed-ratio progression.
   - Start from `start_risk` and `start_lot`.
   - Compute available balance as:
     - `account balance + previous trade profit - minimum equity - already risked amount`
   - Increase the target balance in steps of:
     - `start_delta * current_lot_step`
   - Increase `current_lot_step` by `0.5` each progression step.
   - Increase risk by `start_risk` on each progression step.

3. `Dollar_Risk`
   - Risk the configured dollar amount.
   - Add prior trade profit when that option is enabled.

4. `Percentage`
   - Risk a percentage of available balance.
   - Use `account_per / 100`.
   - Subtract minimum equity and already-risked capital before sizing.

## Strategy-Agnostic Rules

- Treat the sizing module as a pure service that receives entry price, stop loss, order side, and account state.
- Do not assume any entry condition, exit model, session logic, or signal source.
- Keep the sizing code callable from market orders, pending orders, pyramids, scale-ins, and any other execution style.
- Avoid shared state that depends on a specific strategy unless it is passed in explicitly.

## Implementation Rules

- Normalize the final lot to broker volume step.
- Clamp to broker min/max volume.
- Apply the optional user volume limit before order submission.
- Use the margin-level adjustment branch when enabled.
- Reject trades when the calculated size falls to zero or margin checks fail.
- Keep the same direction/type mapping between caller side and order side, but do not infer strategy logic inside the sizing module.

## Porting Checklist

When transplanting the sizing logic into another EA:

1. Add the Summer-style sizing enum and inputs.
2. Copy the fixed-ratio and available-balance helper formulas.
3. Keep prior-profit handling optional.
4. Keep margin and free-margin checks intact.
5. Preserve the final lot normalization and caps.
6. Expose the sizing function through a small adapter or wrapper so any EA can call it.
7. Log the intermediate values when troubleshooting sizing behavior.

## Reference

See [sizing-formulas.md](references/sizing-formulas.md) for the exact formula mapping used in the port.
