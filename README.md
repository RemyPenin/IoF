# GSCI methodology (simplified, pluggable)

This repository contains a practical implementation of the S&P GSCI index mechanics with pluggable inputs for Commodity Production Weights (CPWs), prices, and market disruption events (MDEs). It supports Excess Return (ER) and Total Return (TR) variants.

References:
- S&P GSCI methodology: https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-gsci.pdf
- Commodity index math: https://www.spglobal.com/spdji/en/documents/methodologies/methodology-commodity-index-math.pdf

## Usage

```python
from datetime import date, timedelta
from gsci import GSCIIndexCalculator, IndexMode

# Define inputs
commodities = ["CL", "NG", "GC"]

# CPW: date -> {commodity: weight}
def cpw(d):
    return {"CL": 0.5, "NG": 0.3, "GC": 0.2}

# price: (date, commodity) -> price
def price(d, c):
    # demo price path
    base = {"CL": 80.0, "NG": 3.0, "GC": 1900.0}
    t = d.toordinal()
    return base[c] * (1.0 + 0.0005 * (t % 200))

# mde: (date, commodity) -> bool
def mde(d, c):
    return False

# collateral rate (daily): date -> rate
def rf(d):
    return 0.0001  # 1bp/day

calc = GSCIIndexCalculator(cpw=cpw, price=price, mde=mde, collateral_rate=rf)

dates = [date(2024, 1, 2) + timedelta(days=i) for i in range(10)]
state = calc.compute(dates, initial_level=100.0)

print(state.levels[dates[-1]])
```

Notes:
- This model normalizes CPWs each day, freezes weights for disrupted commodities on disrupted days, and rebalances others to target CPWs. It computes ER returns via price relatives and adds collateral for TR.
- The full S&P GSCI has contract-level rolling rules and other details; this package is structured so you can extend `GSCIIndexCalculator` with more granular roll logic if needed.
