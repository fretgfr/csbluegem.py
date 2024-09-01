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
from typing import List, Literal, NamedTuple, NotRequired, Optional, TypedDict

from .utils import parse_epoch, utcnow

__all__ = ("Screenshots", "PatternData", "SaleMeta", "Sale", "SearchResponse")


class _APISearchMetaDict(TypedDict):
    count: int
    size: int


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


class _APIScreenshotsDict(TypedDict):
    inspect: Optional[str]
    inspect_playside: Optional[str]
    inspect_backside: Optional[str]


class _APISearchSaleDict(TypedDict):
    sale_id: str
    origin: str
    buff_id: int
    date: str
    pattern: int
    float: float
    price: float
    epoch: int
    type: str
    screenshots: _APIScreenshotsDict
    pattern_data: NotRequired[_APIPatternDataDict]
    csfloat: str


class _APISearchResponseDict(TypedDict):
    meta: _APISearchMetaDict
    sales: List[_APISearchSaleDict]


@dataclass
class Screenshots:
    __slots__ = ("_inspect", "inspect_playside", "inspect_backside")

    _inspect: Optional[str]
    inspect_playside: Optional[str]
    inspect_backside: Optional[str]

    @classmethod
    def _from_data(cls, data: _APIScreenshotsDict, /):
        inspect = data["inspect"]
        inspect_playside = data["inspect_playside"]
        inspect_backside = data["inspect_backside"]

        return cls(inspect, inspect_playside, inspect_backside)

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
    def _from_data(cls, data: _APIPatternDataDict, /):
        return cls(**data)


@dataclass
class SaleMeta:
    __slots__ = ("count", "max_sale", "min_sale", "size")

    count: int
    size: int

    @classmethod
    def _from_data(cls, data: _APISearchMetaDict, /):
        count = data["count"]
        size = data["size"]

        return cls(count, size)


@dataclass
class Sale:
    __slots__ = (
        "buff_id",
        "csfloat",
        "_float",
        "type",
        "pattern",
        "timestamp",
        "origin",
        "pattern_data",
        "screenshots",
    )

    buff_id: int
    csfloat: str
    _float: float
    type: str
    pattern: int
    timestamp: datetime.datetime
    origin: str
    pattern_data: Optional[PatternData]
    screenshots: Screenshots

    @classmethod
    def _from_dict(cls, data: _APISearchSaleDict):
        buff_id = data["buff_id"]
        csfloat = data["csfloat"]
        _float = data["float"]
        type = data["type"]
        api_pattern = data["pattern"]
        timestamp = parse_epoch(data["epoch"])
        origin = data["origin"]

        raw_pattern_data: Optional[_APIPatternDataDict] = data.get("pattern_data")
        pattern_data = PatternData._from_data(raw_pattern_data) if raw_pattern_data is not None else None

        raw_screenshots_data: _APIScreenshotsDict = data["screenshots"]
        screenshots = Screenshots._from_data(raw_screenshots_data)

        return cls(buff_id, csfloat, _float, type, api_pattern, timestamp, origin, pattern_data, screenshots)

    @property
    def float(self):
        return self._float

    @property
    def date(self) -> datetime.date:
        return self.timestamp.date()

    @property
    def epoch(self) -> float:
        return self.timestamp.timestamp()

    @property
    def days_since(self) -> int:
        """Returns the number of days since this Sale."""
        return (utcnow() - self.timestamp).days

    @property
    def is_stattrack(self):
        return self.type == "stattrak"


class SearchResponse(NamedTuple):
    meta: SaleMeta
    sales: List[Sale]

    @classmethod
    def _from_data(cls, data: _APISearchResponseDict):
        meta = SaleMeta._from_data(data["meta"])
        sales = [Sale._from_dict(d) for d in data["sales"]]

        return cls(meta, sales)


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
