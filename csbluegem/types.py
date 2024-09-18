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
from typing import TYPE_CHECKING, List, Optional, TypedDict

from .utils import parse_epoch, utcnow

if TYPE_CHECKING:
    from typing_extensions import NotRequired

__all__ = (
    "Screenshots",
    "PatternDataScreenshots",
    "PatternDataExtra",
    "PatternData",
    "SearchMeta",
    "Sale",
    "SearchResponse",
    "Origin",
    "FilterType",
    "Filter",
    "Order",
    "ItemType",
    "Currency",
    "SortKey",
    "Item",
)


class _APISearchMetaDict(TypedDict):
    size: int
    total: int


class _APIPatternDataDict(TypedDict):
    backside_blue: float
    backside_contour_blue: int
    backside_contour_purple: int
    backside_gold: float
    backside_purple: float
    playside_blue: float
    playside_contour_blue: int
    playside_contour_purple: float
    playside_gold: float
    playside_purple: float
    pattern: NotRequired[int]
    quantity: NotRequired[int]
    screenshots: NotRequired[_APIPatternDataScreenshots]
    extra: NotRequired[_APIPatternDataExtras]


class _APISearchScreenshotsDict(TypedDict):
    inspect: Optional[str]
    inspect_playside: Optional[str]
    inspect_backside: Optional[str]


class _APISearchSaleDict(TypedDict):
    sale_id: str
    origin: Origin
    buff_id: int
    date: str
    pattern: int
    wear: float
    price: float
    epoch: int
    steam_inspect_link: str
    type: str
    screenshots: _APISearchScreenshotsDict
    pattern_data: NotRequired[_APIPatternDataDict]
    csfloat: str


class _APIPatternDataScreenshots(TypedDict):
    csbluegem_screenshot: str
    aq_oiled: str


class _APIPatternDataExtras(TypedDict):
    similar_playside: str
    similar_backside: str
    csfloat_link: str
    search: str


class _APISearchResponseDict(TypedDict):
    meta: _APISearchMetaDict
    sales: List[_APISearchSaleDict]


class _APIPatternDataResponseDict(TypedDict):
    meta: _APISearchMetaDict
    data: List[_APIPatternDataDict]


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
    def _from_data(cls, data: _APISearchScreenshotsDict, /):
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
class PatternDataScreenshots:
    """Screenshots that may be associated with this :class:`~csbluegem.types.PatternData`.

    Only available when using :meth:`~csbluegem.client.Client.pattern_data`.

    Attributes
    ----------
    backside_blue: :class:`float`
        The percentage of blue visible on the back side.
    """

    __slots__ = ("csbluegem_screenshot", "aq_oiled")

    csbluegem_screenshot: str
    aq_oiled: str

    @classmethod
    def _from_data(cls, data: _APIPatternDataScreenshots, /):
        return cls(**data)


@dataclass
class PatternDataExtra:
    """Extra information provided for pattern data.

    Only available when using :meth:`~csbluegem.client.Client.pattern_data`.

    Attributes
    ----------
    similar_playside: :class:`str`
        A URL to an image of an item with a similar playside.
    similar_backside: :class:`str`
        A URL to an image of an item with a similar backside.
    csfloat_link: :class:`str`
        The CSFloat database query for this pattern.
    search: :class:`str`
        A URL to a search for this pattern.
    """

    __slots__ = ("similar_playside", "similar_backside", "csfloat_link", "search")

    similar_playside: str
    similar_backside: str
    csfloat_link: str
    search: str

    @classmethod
    def _from_data(cls, data: _APIPatternDataExtras, /):
        return cls(**data)


@dataclass
class PatternData:
    """Data for a pattern on CSBlueGem.

    Attributes
    ----------
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
    pattern: Optional[:class:`int`]
        The pattern represented by this PatternData.
    quantity: Optional[:class:`int`]
        The number of sales attributed to this PatternData.
    screenshots: Optional[:class:`~csbluegem.types.PatternDataScreenshots`]
        Example screenshots of the pattern associated with this PatternData on in game items.
    extra: Optional[:class:`~csbluegem.types.PatternDataExtra`]
        Extra information about this PatternData.
    """

    __slots__ = (
        "backside_blue",
        "backside_contour_blue",
        "backside_contour_purple",
        "backside_gold",
        "backside_purple",
        "playside_blue",
        "playside_contour_blue",
        "playside_contour_purple",
        "playside_gold",
        "playside_purple",
        "pattern",
        "quantity",
        "screenshots",
        "extra",
    )

    backside_blue: float
    backside_contour_blue: int
    backside_contour_purple: int
    backside_gold: float
    backside_purple: float
    playside_blue: float
    playside_contour_blue: int
    playside_contour_purple: float
    playside_gold: float
    playside_purple: float
    pattern: Optional[int]
    quantity: Optional[int]
    screenshots: Optional[PatternDataScreenshots]
    extra: Optional[PatternDataExtra]

    @classmethod
    def _from_data(cls, data: _APIPatternDataDict, /):
        backside_blue = data["backside_blue"]
        backside_contour_blue = data["backside_contour_blue"]
        backside_contour_purple = data["backside_contour_purple"]
        backside_gold = data["backside_gold"]
        backside_purple = data["backside_purple"]
        playside_blue = data["playside_blue"]
        playside_contour_blue = data["playside_contour_blue"]
        playside_contour_purple = data["playside_contour_purple"]
        playside_gold = data["playside_gold"]
        playside_purple = data["playside_purple"]
        pattern = data.get("pattern")
        quantity = data.get("quantity")
        screenshots_dict = data.get("screenshots")
        extra_dict = data.get("extra")

        screenshots = PatternDataScreenshots._from_data(screenshots_dict) if screenshots_dict is not None else None
        extra = PatternDataExtra._from_data(extra_dict) if extra_dict is not None else None

        return cls(
            backside_blue,
            backside_contour_blue,
            backside_contour_purple,
            backside_gold,
            backside_purple,
            playside_blue,
            playside_contour_blue,
            playside_contour_purple,
            playside_gold,
            playside_purple,
            pattern,
            quantity,
            screenshots,
            extra,
        )


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

    __slots__ = ("size", "total")

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
    wear: :class:`float`
        The float of the item.
    type: :class:`~csbluegem.types.ItemType`
        The type of the item.
    pattern: :class:`int`
        The pattern of the item.
    timestamp: :class:`datetime.datetime`
        When the sale occurred.
    steam_inspect_link: :class:`str`
        The inspect link for this item.
    origin: :class:`~csbluegem.types.Origin`
        Where the sale data originated.
    pattern_data: Optional[:class:`~csbluegem.types.PatternData`]
        The pattern data for the item, if available.
    screenshots: :class:`~csbluegem.types.Screenshots`
        Screenshot data for the item.
    """

    __slots__ = (
        "buff_id",
        "csfloat",
        "wear",
        "type",
        "pattern",
        "price",
        "timestamp",
        "steam_inspect_link",
        "origin",
        "pattern_data",
        "screenshots",
    )

    buff_id: int
    csfloat: str
    wear: float
    type: ItemType
    pattern: int
    price: float
    timestamp: datetime.datetime
    steam_inspect_link: str
    origin: Origin
    pattern_data: Optional[PatternData]
    screenshots: Screenshots

    @classmethod
    def _from_data(cls, data: _APISearchSaleDict):
        buff_id = data["buff_id"]
        csfloat = data["csfloat"]
        wear = data["wear"]
        type = ItemType(data["type"])
        api_pattern = data["pattern"]
        price = data["price"]
        timestamp = parse_epoch(data["epoch"])
        steam_inspect_link = data["steam_inspect_link"]
        origin = Origin(data["origin"])

        raw_pattern_data: Optional[_APIPatternDataDict] = data.get("pattern_data")
        pattern_data = PatternData._from_data(raw_pattern_data) if raw_pattern_data is not None else None

        raw_screenshots_data: _APISearchScreenshotsDict = data["screenshots"]
        screenshots = Screenshots._from_data(raw_screenshots_data)

        return cls(
            buff_id,
            csfloat,
            wear,
            type,
            api_pattern,
            price,
            timestamp,
            steam_inspect_link,
            origin,
            pattern_data,
            screenshots,
        )

    @property
    def float(self):
        """The float of the item."""
        return self.wear

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
    def is_stattrak(self) -> bool:
        """Whether the item was stattrak"""
        return self.type is ItemType.StatTrak


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
        sales = [Sale._from_data(d) for d in data["sales"]]

        return cls(meta, sales)


@dataclass
class PatternDataResponse:
    """Represents a response to a pattern data query.

    Attributes
    ----------
    meta: :class:`~csbluegem.types.SearchMeta`
        Metadata about the query.
    data: List[:class:`~csbluegem.types.PatternData`]
        The pattern datas that were returned.
    """

    __slots__ = ("meta", "pattern_data")

    meta: SearchMeta
    pattern_data: List[PatternData]

    @classmethod
    def _from_data(cls, api_data: _APIPatternDataResponseDict):
        meta = SearchMeta._from_data(api_data["meta"])
        pattern_data = [PatternData._from_data(d) for d in api_data["data"]]

        return cls(meta, pattern_data)


class Origin(Enum):
    """Where a :class:`~csbluegem.types.Sale` originated from."""

    # fmt: off
    Buff     = "Buff"
    CSFloat  = "CSFloat"
    SkinBid  = "SkinBid"
    BroSkins = "BroSkins"
    Skinport = "Skinport"
    C5Game   = "c5game"
    # fmt: on

    def __str__(self) -> str:
        """Returns the value of the member."""
        return self.value


class FilterType(Enum):
    """What a :class:`~csbluegem.types.Filter` should filter by."""

    # fmt: off
    PlaysideBlue   = "playside_blue"
    PlaysidePurple = "playside_purple"
    PlaysideGold   = "playside_gold"
    BacksideBlue   = "backside_blue"
    BacksidePurple = "backside_purple"
    BacksideGold   = "backside_gold"
    # fmt: on


class Filter:
    """A filter for searches.

    Attributes
    ----------
    type: :class:`~csbluegem.types.FilterType`
        What kind of filter.
    min: :class:`float`
        The minimum value for this filter.
    max: :class:`float`
        The maximum value for this filter.
    """

    __slots__ = ("type", "min", "max")

    def __init__(self, type: FilterType, min: float, max: float):
        self.type = type
        self.min = min
        self.max = max

    def _is_valid(self):
        return (0 <= self.min < 100 and 0 < self.max <= 100) and self.max > self.min


class Order(Enum):
    """How query results should be ordered."""

    # fmt: off
    Asc  = "ASC"
    Desc = "DESC"
    # fmt: on


class ItemType(Enum):
    """The type of an item."""

    # fmt: off
    StatTrak = "stattrak"
    Normal   = "normal"
    # fmt: on


class Currency(Enum):
    """Available currencies for use in the API."""

    USD = "USD"
    EUR = "EUR"
    JPY = "JPY"
    GBP = "GBP"
    CNY = "CNY"
    AUD = "AUD"
    CAD = "CAD"


class SortKey(Enum):
    """How the results of a query should be sorted."""

    # fmt: off
    PlaysideBlue          = "playside_blue"
    PlaysidePurple        = "playside_purple"
    PlaysideGold          = "playside_gold"
    BacksideBlue          = "backside_blue"
    BacksidePurple        = "backside_purple"
    BacksideGold          = "backside_gold"
    PlaysideContourBlue   = "playside_contour_blue"
    PlaysideContourPurple = "playside_contour_purple"
    BacksideContourBlue   = "backside_contour_blue"
    BacksideContourPurple = "backside_contour_purple"
    Pattern               = "pattern"
    Wear                  = "wear"
    Date                  = "date"
    Price                 = "price"
    # fmt: on


class Item(Enum):
    """Items that can be queried from the API."""

    # fmt: off
    AK47           = "AK-47"
    Bayonet        = "Bayonet"
    BowieKnife     = "Bowie Knife"
    ButterflyKnife = "Butterfly Knife"
    ClassicKnife   = "Classic Knife"
    FalchionKnife  = "Falchion Knife"
    FiveSeveN      = "Five-SeveN"
    FlipKnife      = "Flip Knife"
    GutKnife       = "Gut Knife"
    HuntsmanKnife  = "Huntsman Knife"
    HydraGloves    = "Hydra Gloves"
    Karambit       = "Karambit"
    KukriKnife     = "Kukri Knife"
    M9Bayonet      = "M9 Bayonet"
    MAC10          = "MAC-10"
    NavajaKnife    = "Navaja Knife"
    NomadKnife     = "Nomad Knife"
    ParacordKnife  = "Paracord Knife"
    ShadowDaggers  = "Shadow Daggers"
    SkeletonKnife  = "Skeleton Knife"
    StilettoKnife  = "Stiletto Knife"
    SurvivalKnife  = "Survival Knife"
    TalonKnife     = "Talon Knife"
    UrsusKnife     = "Ursus Knife"
    # fmt: on
