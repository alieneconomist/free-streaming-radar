# Summer EA Sizing Formulas

## Fixed Lot

Return the configured lot size directly.

## Dynamic

Use the fixed-ratio progression:

```text
available_balance = account_balance + previous_trade_profit - minimum_equity - already_risked_amount

target_balance = start_balance
final_risk = start_risk
current_lot_step = start_lot

while available_balance > target_balance:
    target_balance += start_delta * current_lot_step
    if target_balance >= available_balance:
        stop and use final_risk
    current_lot_step += 0.5
    final_risk += start_risk
```

## Dollar Risk

Use the configured dollar amount.

If prior-profit inclusion is enabled, add the last closed trade profit before sizing.

## Percentage

```text
available_balance = account_balance + previous_trade_profit - minimum_equity - already_risked_amount
risk_money = available_balance * account_per / 100
lot_size = risk_money / money_lot_step
```

Where:

```text
money_lot_step = (abs(entry - stoploss) / tick_size) * tick_value * lot_step
```

## Shared Guards

- Reject zero or negative sizes.
- Clamp to broker min/max volume.
- Respect optional user volume limit.
- Resize for minimum margin level when enabled.
- Stop when free margin is insufficient.
