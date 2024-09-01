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
from enum import Enum
from typing import List, Literal, NotRequired, Optional, TypedDict

from .utils import parse_epoch, utcnow

__all__ = ("Screenshots", "PatternData", "SearchMeta", "Sale", "SearchResponse", "SaleOrigin")


class _APISearchMetaDict(TypedDict):
    size: int
    total: int


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
    origin: SaleOrigin
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


class SaleOrigin(Enum):
    """Where a :class:`~csbluegem.types.Sale` originated from."""

    Buff = "Buff"
    CSFloat = "CSFloat"
    SkinBid = "SkinBid"
    BroSkins = "BroSkins"


@dataclass
class Screenshots:
    """Screenshots for a :class:`~csbluegem.types.Sale`.

    Attributes
    ----------
    inspect: :class:`str`
        A url to an inspect link. Always returns a url for an inspect link.

        For CSFloat based sales, this returns the playside inspect link.
    inspect_playside: Optional[:class:`str`]
        A url to the playside inspect link. Only applicable for CSFloat sales.
    inspect_backside: Optional[:class:`str`]
        A url to the backside inspect link. Only applicable for CSFloat sales.
    """

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
    """Data for a pattern on CSBlueGem.

    Attributes
    ----------
    aq_oiled: :class:`str`
        A URL to a screenshot with the skin over the aq oiled template.
    backside_blue: :class:`float`
        The percentage of blue visible on the back side.
    backside_contour_blue: :class:`int`
        The number of individual blue sections visible on the back side.
    backside_contour_purple: :class:`int`
        The number of individual purple sections visible on the back side.
    backside_gold: :class:`float`
        The percentage of gold visible on the back side.
    backside_purple: :class:`float`
        The percentage of purple visible on the back side.
    csbluegem_screenshot: :class:`str`
        A URL to a sample screenshot of the pattern.
    playside_blue: :class:`float`
        The percentage of blue visible on the back side.
    playside_contour_blue: :class:`int`
        The number of individual blue sections visible on the play side.
    playside_contour_purple: :class:`int`
        The number of individual purple sections visible on the play side.
    playside_gold: :class:`float`
        The percentage of gold visible on the play side.
    playside_purple: :class:`float`
        The percentage of purple visible on the play side.
    """

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
class SearchMeta:
    """Metadata about the search.

    Attributes
    ----------
    size: :class:`int`
        The number of items returned.
    total: :class:`int`
        The total number of items available.
    """

    __slots__ = ("count", "max_sale", "min_sale", "size")

    size: int
    total: int

    @classmethod
    def _from_data(cls, data: _APISearchMetaDict, /):
        size = data["size"]
        total = data["total"]

        return cls(size, total)


@dataclass
class Sale:
    """Represents a record of sale from CSBlueGem

    Attributes
    ----------
    buff_id: :class:`int`
        The id of the item on Buff.
    csfloat: :class:`str`
        A link to the item on CSFloat.
    float: :class:`float`
        The float of the item.
    type: :class:`str`
        The type of the item. Can either be "normal" or "stattrak".
    pattern: :class:`int`
        The pattern of the item.
    timestamp: :class:`datetime.datetime`
        When the sale occurred.
    origin: :class:`~csbluegem.types.SaleOrigin`
        Where the sale data originated.
    pattern_data: Optional[:class:`~csbluegem.types.PatternData`]
        The pattern data for the item, if available.
    screenshots: :class:`~csbluegem.types.Screenshots`
        Screenshot data for the item.
    """

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
    origin: SaleOrigin
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
        origin = SaleOrigin(data["origin"])

        raw_pattern_data: Optional[_APIPatternDataDict] = data.get("pattern_data")
        pattern_data = PatternData._from_data(raw_pattern_data) if raw_pattern_data is not None else None

        raw_screenshots_data: _APIScreenshotsDict = data["screenshots"]
        screenshots = Screenshots._from_data(raw_screenshots_data)

        return cls(buff_id, csfloat, _float, type, api_pattern, timestamp, origin, pattern_data, screenshots)

    @property
    def float(self):
        """The float of the item."""
        return self._float

    @property
    def date(self) -> datetime.date:
        """The date this item was sold."""
        return self.timestamp.date()

    @property
    def epoch(self) -> float:
        """The epoch the item was sold."""
        return self.timestamp.timestamp()

    @property
    def days_since(self) -> int:
        """Returns the number of days since this Sale."""
        return (utcnow() - self.timestamp).days

    @property
    def is_stattrack(self) -> bool:
        """Whether the item was stattrak"""
        return self.type == "stattrak"


@dataclass
class SearchResponse:
    """Represents a response to a search query.

    Attributes
    ----------
    meta: :class:`~csbluegem.types.SearchMeta`
        Metadata about the query.
    sales: List[:class:`~csbluegem.types.Sale`]
        The sales that were returned.
    """

    __slots__ = ("meta", "sales")

    meta: SearchMeta
    sales: List[Sale]

    @classmethod
    def _from_data(cls, data: _APISearchResponseDict):
        meta = SearchMeta._from_data(data["meta"])
        sales = [Sale._from_dict(d) for d in data["sales"]]

        return cls(meta, sales)


BlueGemItem = Literal[  # TODO Should probably be an enum
    "AK-47",
    "Bayonet",
    "Bowie Knife",
    "Butterfly Knife",
    "Classic Knife",
    "Falchion Knife",
    "Five-SeveN",
    "Flip Knife",
    "Gut Knife",
    "Huntsman Knife",
    "Hydra Gloves",
    "Karambit",
    "Kukri Knife",
    "M9 Bayonet",
    "MAC-10",
    "Navaja Knife",
    "Nomad Knife",
    "Paracord Knife",
    "Shadow Daggers",
    "Skeleton Knife",
    "Stiletto Knife",
    "Survival Knife",
    "Talon Knife",
    "Ursus Knife",
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

Order = Literal["ascending", "descending"]  # TODO Should probably be an enum
ItemType = Literal["any", "stattrack", "normal"]  # TODO Should probably be an enum
Currency = Literal["USD", "EUR", "JPY", "GBP", "CNY", "AUD", "CAD"]  # TODO Should probably be an enum
Origin = Literal["any", "Buff", "CSFloat", "SkinBid", "BroSkins"]  # TODO Should probably be an enum

SortKey = Literal[  # TODO Should probably be an enum
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

BlueGemKnives = Literal[  # TODO Should probably be an enumO
    "Bayonet",
    "Bowie Knife",
    "Butterfly Knife",
    "Classic Knife",
    "Falchion Knife",
    "Flip Knife",
    "Gut Knife",
    "Huntsman Knife",
    "Karambit",
    "Kukri Knife",
    "M9 Bayonet",
    "Navaja Knife",
    "Nomad Knife",
    "Paracord Knife",
    "Shadow Daggers",
    "Skeleton Knife",
    "Stiletto Knife",
    "Survival Knife",
    "Talon Knife",
    "Ursus Knife",
]
