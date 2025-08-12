from datetime import date, timedelta

from gsci import GSCIIndexCalculator, IndexMode
from gsci.index import GSCIConfig

commodities = ["CL", "NG", "GC"]


def cpw(d):
    # Constant CPWs for demo; in practice these are annual and may change at reconstitution
    return {"CL": 0.55, "NG": 0.25, "GC": 0.20}


def price(d, c):
    # Simple deterministic drift to verify monotonicity
    base = {"CL": 80.0, "NG": 3.0, "GC": 1900.0}
    day = d.toordinal()
    drift = {"CL": 0.0006, "NG": 0.0003, "GC": 0.0002}
    return base[c] * (1.0 + drift[c] * (day % 200))


def mde(d, c):
    # No disruptions in demo
    return False


def rf(d):
    # 1bp/day
    return 0.0001


if __name__ == "__main__":
    dates = [date(2024, 1, 2) + timedelta(days=i) for i in range(15)]

    calc_er = GSCIIndexCalculator(cpw=cpw, price=price, mde=mde)
    state_er = calc_er.compute(dates, initial_level=100.0)

    cfg_tr = GSCIConfig(mode=IndexMode.TOTAL_RETURN)
    calc_tr = GSCIIndexCalculator(cpw=cpw, price=price, mde=mde, collateral_rate=rf, config=cfg_tr)
    state_tr = calc_tr.compute(dates, initial_level=100.0)

    print("ER end level:", round(state_er.levels[dates[-1]], 6))
    print("TR end level:", round(state_tr.levels[dates[-1]], 6))