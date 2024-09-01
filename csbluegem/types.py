"""
Copyright 2024-present fretgfr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Any, Dict, Literal, Optional, TypedDict, Union

from .utils import parse_date, utcnow

__all__ = (
    "Screenshots",
    "Sale",
)


class _APIPatternDataDict(TypedDict):
    aq_oiled: str
    backside_blue: float
    backside_contour_blue: int
    backside_contour_purple: int
    backside_gold: float
    backside_purple: float
    csbluegem_screenshot: str
    playside_blue: float
    playside_contour_blue: int
    playside_contour_purple: float
    playside_gold: float
    playside_purple: float


class _APISaleDataDict(TypedDict):
    date: str
    origin: str
    inspect: str
    price: float


class _APIScreenshotsDict(TypedDict):
    inspect: Optional[str]
    inspect_playside: Optional[str]
    inspect_backside: Optional[str]


@dataclass
class Screenshots:
    __slots__ = ("sale", "_inspect", "inspect_playside", "inspect_backside")

    sale: Sale
    _inspect: Optional[str]
    inspect_playside: Optional[str]
    inspect_backside: Optional[str]

    @classmethod
    def _from_data(cls, sale: Sale, /, *, data: _APIScreenshotsDict):
        inspect = data["inspect"]
        inspect_playside = data["inspect_playside"]
        inspect_backside = data["inspect_backside"]

        return cls(sale, inspect, inspect_playside, inspect_backside)

    @property
    def inspect(self) -> str:
        """Returns an inspect link no matter where the underlying :class:`~csbluegem.types.Sale` originated.

        For CSFloat based Sales, this will return the playside inspect link.
        """

        if self._inspect:
            return self._inspect

        if self.inspect_playside:
            return self.inspect_playside

        raise RuntimeError("invalid data was received from the API")


@dataclass
class PatternData:

    __slots__ = (
        "aq_oiled",
        "backside_blue",
        "backside_contour_blue",
        "backside_contour_purple",
        "backside_gold",
        "backside_purple",
        "csbluegem_screenshot",
        "playside_blue",
        "playside_contour_blue",
        "playside_contour_purple",
        "playside_gold",
        "playside_purple",
    )

    aq_oiled: str
    backside_blue: float
    backside_contour_blue: int
    backside_contour_purple: int
    backside_gold: float
    backside_purple: float
    csbluegem_screenshot: str
    playside_blue: float
    playside_contour_blue: int
    playside_contour_purple: float
    playside_gold: float
    playside_purple: float

    @classmethod
    def _from_data(cls, data: _APIPatternDataDict):
        return cls(**data)


@dataclass
class SaleData:
    __slots__ = ("timestamp", "origin", "inspect", "price")

    timestamp: datetime.datetime
    origin: str
    inspect: str
    price: float

    @classmethod
    def _from_data(cls, data: _APISaleDataDict):
        date = parse_date(data["date"])
        origin = data["origin"]
        inspect = data["inspect"]
        price = data["price"]

        return cls(date, origin, inspect, price)

    @property
    def date(self) -> datetime.date:
        return self.timestamp.date()

    @property
    def days_since(self) -> int:
        """The number of days since this sale."""
        return (utcnow() - self.timestamp).days


@dataclass
class Sale:
    __slots__ = ("_float", "is_stattrak", "pattern", "origin", "date", "price")

    buff_id: int
    csfloat: str
    _float: float
    is_stattrak: bool
    pattern: int
    pattern_data: Optional[PatternData]
    sale_data: Optional[SaleData]

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        buff_id = data["buff_id"]
        csfloat = data["csfloat"]
        _float = data["float"]
        is_stattrak = data["isStattrak"]
        api_pattern = data["pattern"]

        raw_pattern_data: Optional[_APIPatternDataDict] = data.get("pattern_data")
        pattern_data = PatternData._from_data(raw_pattern_data) if raw_pattern_data is not None else None

        raw_sale_data: Optional[_APISaleDataDict] = data.get("sale_data")
        sale_data = SaleData._from_data(raw_sale_data) if raw_sale_data is not None else None

        return cls(buff_id, csfloat, _float, is_stattrak, api_pattern, pattern_data, sale_data)

    @property
    def float(self):
        return self._float


BlueGemItem = Literal[
    "AK-47",
    "Bayonet",
    "Bowie_Knife",
    "Butterfly_Knife",
    "Classic_Knife",
    "Falchion_Knife",
    "Five-SeveN",
    "Flip_Knife",
    "Gut_Knife",
    "Huntsman_Knife",
    "Hydra_Gloves",
    "Karambit",
    "Kukri_Knife",
    "M9_Bayonet",
    "MAC-10",
    "Navaja_Knife",
    "Nomad_Knife",
    "Paracord_Knife",
    "Shadow_Daggers",
    "Skeleton_Knife",
    "Stiletto_Knife",
    "Survival_Knife",
    "Talon_Knife",
    "Ursus_Knife",
]


Filter = Literal[
    "playside_blue",
    "playside_purple",
    "playside_gold",
    "backside_blue",
    "backside_purple",
    "backside_gold",
    "playside_contour_blue",
    "playside_contour_purple",
    "backside_contour_blue",
    "backside_contour_purple",
]

Order = Literal["ascending", "descending"]
ItemType = Literal["any", "stattrack", "normal"]
Currency = Literal["USD", "EUR", "JPY", "GBP", "CNY", "AUD", "CAD"]
Origin = Literal["any", "Buff", "CSFloat", "SkinBid", "BroSkins"]

SortKey = Literal[
    "playside_blue",
    "playside_purple",
    "playside_gold",
    "backside_blue",
    "backside_purple",
    "backside_gold",
    "playside_contour_blue",
    "playside_contour_purple",
    "backside_contour_blue",
    "backside_contour_purple",
    "pattern",
    "float",
    "date",
    "price",
]

BlueGemKnives = Literal[
    "Bayonet",
    "Bowie_Knife",
    "Butterfly_Knife",
    "Classic_Knife",
    "Falchion_Knife",
    "Flip_Knife",
    "Gut_Knife",
    "Huntsman_Knife",
    "Karambit",
    "Kukri_Knife",
    "M9_Bayonet",
    "Navaja_Knife",
    "Nomad_Knife",
    "Paracord_Knife",
    "Shadow_Daggers",
    "Skeleton_Knife",
    "Stiletto_Knife",
    "Survival_Knife",
    "Talon_Knife",
    "Ursus_Knife",
]
