from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

from .types import (
    CPWFunction,
    CollateralRateFunction,
    CommodityId,
    DateLike,
    IndexMode,
    MDEFunction,
    PriceFunction,
    IndexState,
)


def _to_date(d: DateLike) -> date:
    if isinstance(d, date) and not isinstance(d, datetime):
        return d
    if isinstance(d, datetime):
        return d.date()
    # assume ISO string
    return datetime.fromisoformat(str(d)).date()


def _normalize(weights: Mapping[CommodityId, float]) -> Mapping[CommodityId, float]:
    nonneg = {c: max(0.0, float(w)) for c, w in weights.items()}
    s = sum(nonneg.values())
    if s <= 0:
        return {c: 0.0 for c in nonneg.keys()}
    return {c: w / s for c, w in nonneg.items()}


def _maps_close(a: Mapping[str, float], b: Mapping[str, float], tol: float = 1e-10) -> bool:
    keys = set(a.keys()) | set(b.keys())
    for k in keys:
        av = float(a.get(k, 0.0))
        bv = float(b.get(k, 0.0))
        if abs(av - bv) > tol:
            return False
    return True


@dataclass
class GSCIConfig:
    start_level: float = 100.0
    mode: IndexMode = IndexMode.EXCESS_RETURN


class GSCIIndexCalculator:
    """Implements a practical S&P GSCI-like methodology core with buy-and-hold quantities
    between reconstitutions (CPW changes), MDE-aware reconstitution, and optional collateral.

    Assumptions/simplifications for portability:
    - CPWs per date are provided externally via cpw(date) -> {commodity: weight}.
      Typically these change annually; we reconstitute whenever the CPW map changes.
    - Prices are provided via price(date, commodity); contract-level roll is not modeled
      here. If your price series embeds the official roll, the index will align better.
    - Market disruption events (MDE) are provided via mde(date, commodity) -> bool.
      On disrupted days, we use prior valid price for return calc and freeze quantities for
      reconstitution in that commodity.
    - ER index: portfolio valued by quantities; return = V_t / V_{t-1} - 1
    - TR index: ER plus collateral at risk-free rate applied to prior day index level
    """

    def __init__(
        self,
        cpw: CPWFunction,
        price: PriceFunction,
        mde: MDEFunction,
        collateral_rate: Optional[CollateralRateFunction] = None,
        config: Optional[GSCIConfig] = None,
    ) -> None:
        self.cpw = cpw
        self.price = price
        self.mde = mde
        self.collateral_rate = collateral_rate
        self.config = config or GSCIConfig()

    def compute(
        self,
        dates: Sequence[DateLike],
        initial_level: Optional[float] = None,
    ) -> IndexState:
        if not dates:
            raise ValueError("dates must be non-empty")
        date_list: List[date] = sorted(_to_date(d) for d in dates)

        state: IndexState = IndexState(levels={}, weights={}, quantities={}, price_cache={})
        level = float(initial_level or self.config.start_level)

        # Initialize at t0: set quantities per CPW(t0) using t0 prices
        t0 = date_list[0]
        cpw_t0 = _normalize(self.cpw(t0))
        p_t0 = {c: self._get_price(state, t0, c) for c in cpw_t0.keys()}
        # Initial portfolio value equals index level
        quantities_t0: MutableMapping[CommodityId, float] = {}
        for c, w in cpw_t0.items():
            price_c = p_t0[c]
            qty = 0.0 if price_c == 0 else (w * level) / price_c
            quantities_t0[c] = qty
        weights_t0 = self._weights_from_quantities(quantities_t0, p_t0)

        state.levels[t0] = level
        state.quantities[t0] = dict(quantities_t0)
        state.weights[t0] = dict(weights_t0)

        # Iterate forward
        for t_prev, t in zip(date_list[:-1], date_list[1:]):
            quantities_prev = state.quantities[t_prev]

            # Prices
            p_prev = {c: self._get_price(state, t_prev, c) for c in quantities_prev.keys()}
            # Use previous holdings set as the universe; allow new names only on reconstitution
            # Effective t prices for return calc (freeze disrupted)
            p_eff_t: MutableMapping[CommodityId, float] = {}
            for c in quantities_prev.keys():
                p_t = self._get_price(state, t, c)
                p_eff_t[c] = p_prev[c] if self.mde(t, c) else p_t

            # Previous portfolio value
            value_prev = sum(quantities_prev[c] * p_prev[c] for c in quantities_prev.keys())
            if value_prev <= 0:
                er_return = 0.0
            else:
                value_t = sum(quantities_prev[c] * p_eff_t[c] for c in quantities_prev.keys())
                er_return = (value_t / value_prev) - 1.0

            level_new = level * (1.0 + er_return)

            # Total return collateral component: apply overnight collateral on prior level
            if self.config.mode == IndexMode.TOTAL_RETURN:
                if self.collateral_rate is None:
                    raise ValueError("TR mode requires collateral_rate callable")
                r = self.collateral_rate(t_prev)  # simple daily rate
                level_new *= (1.0 + r)

            # Determine if reconstitution occurs at t (CPW change)
            cpw_prev = _normalize(self.cpw(t_prev))
            cpw_now = _normalize(self.cpw(t))
            is_reconstitution = not _maps_close(cpw_prev, cpw_now)

            # Set quantities for end of t (after any reconstitution at t open)
            if is_reconstitution:
                # Reconstitute at t open using p_prev. Freeze disrupted commodities' quantities
                # and reallocate remaining notional among non-disrupted to target CPW(t).
                disrupted = {c for c in set(cpw_prev.keys()) | set(cpw_now.keys()) if self.mde(t, c)}

                # Universe update: include any new commodities in CPW(now)
                all_commodities = set(quantities_prev.keys()) | set(cpw_now.keys())

                # Compute previous portfolio value by commodity
                prev_values = {c: quantities_prev.get(c, 0.0) * p_prev.get(c, self._safe_price(state, t_prev, c)) for c in all_commodities}
                total_prev = sum(prev_values.values())

                # Fixed notional for disrupted: keep previous quantities
                fixed_notional = sum(prev_values.get(c, 0.0) for c in disrupted)

                # Target weights for non-disrupted, renormalized
                non_disrupted = [c for c in all_commodities if c not in disrupted]
                target_non_disrupted = {c: cpw_now.get(c, 0.0) for c in non_disrupted}
                target_non_disrupted = _normalize(target_non_disrupted)

                # Remaining notional to allocate
                remaining_notional = max(total_prev - fixed_notional, 0.0)

                quantities_t: MutableMapping[CommodityId, float] = {}

                # Disrupted: keep previous quantities
                for c in disrupted:
                    quantities_t[c] = quantities_prev.get(c, 0.0)

                # Non-disrupted: set quantities to meet target weights on remaining notional at p_prev
                for c in non_disrupted:
                    w = target_non_disrupted.get(c, 0.0)
                    p_c_prev = p_prev.get(c, self._safe_price(state, t_prev, c))
                    notional_c = w * remaining_notional
                    qty_c = 0.0 if p_c_prev == 0 else notional_c / p_c_prev
                    quantities_t[c] = qty_c
            else:
                # No reconstitution: keep quantities
                quantities_t = dict(quantities_prev)

            # Compute weights at end of day using effective close prices (consistent with level move)
            weights_t = self._weights_from_quantities(quantities_t, p_eff_t)

            # Update state
            level = level_new
            state.levels[t] = level_new
            state.quantities[t] = dict(quantities_t)
            state.weights[t] = dict(weights_t)

        return state

    # Helpers
    def _get_price(self, state: IndexState, d: date, c: CommodityId) -> float:
        key = (d, c)
        if key not in state.price_cache:
            state.price_cache[key] = float(self.price(d, c))
        return state.price_cache[key]

    def _safe_price(self, state: IndexState, d: date, c: CommodityId) -> float:
        # If price is unavailable for a new commodity on prev date, fallback to 1.0 to avoid crash
        try:
            return self._get_price(state, d, c)
        except Exception:
            return 1.0

    def _weights_from_quantities(
        self,
        quantities: Mapping[CommodityId, float],
        prices: Mapping[CommodityId, float],
    ) -> Mapping[CommodityId, float]:
        values = {c: quantities.get(c, 0.0) * prices.get(c, 0.0) for c in set(quantities.keys()) | set(prices.keys())}
        total = sum(v for v in values.values())
        if total <= 0:
            return {c: 0.0 for c in values.keys()}
        return {c: (v / total) for c, v in values.items()}