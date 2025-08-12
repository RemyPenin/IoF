from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Callable, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple, Union

# Basic identifiers
CommodityId = str
ContractId = str
DateLike = Union[date, datetime, str]

# External data providers (to be injected)
CPWFunction = Callable[[DateLike], Mapping[CommodityId, float]]
PriceFunction = Callable[[DateLike, CommodityId], float]
MDEFunction = Callable[[DateLike, CommodityId], bool]
CollateralRateFunction = Callable[[DateLike], float]


class IndexMode(Enum):
    EXCESS_RETURN = "ER"
    TOTAL_RETURN = "TR"


@dataclass
class RollSchedule:
    """Defines roll parameters for a commodity.

    Note: The full S&P GSCI has complex rolling heuristics (dynamic roll periods
    per commodity/contract month). Here we keep a pluggable structure so users can
    customize. By default, we assume daily constant maturity roll with roll_weight
    provided externally or zero (no roll) if not used.
    """

    roll_start_day_of_month: int = 5
    roll_window_length_days: int = 5


@dataclass
class IndexState:
    """Holds the evolving index state across dates.

    - levels: overall index level per date
    - weights: current target weights per commodity per date (after MDE handling)
    - quantities: index "units" held per commodity (notional exposures), updated for roll
    - price_cache: optional price cache to avoid repeated calls
    """

    levels: MutableMapping[date, float]
    weights: MutableMapping[date, Mapping[CommodityId, float]]
    quantities: MutableMapping[date, Mapping[CommodityId, float]]
    price_cache: MutableMapping[Tuple[date, CommodityId], float]