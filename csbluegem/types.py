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
from typing import Any, Dict, Literal

from .utils import parse_date, utcnow

__all__ = ("Sale",)


@dataclass
class Sale:
    __slots__ = ("_float", "is_stattrak", "pattern", "origin", "date", "price")

    _float: float
    is_stattrak: bool
    pattern: int
    origin: str
    timestamp: datetime.datetime
    price: float
    # TODO INCOMPLETE

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        _float = data["float"]
        is_stattrak = data["isStattrak"]
        api_pattern = data["pattern"]
        origin = data["sale_info"]["origin"]
        date = parse_date(data["sale_info"]["date"])
        price = float(data["sale_info"]["price"])
        # TODO INCOMPLETE

        return cls(_float, is_stattrak, api_pattern, origin, date, price)

    @property
    def float(self):
        return self._float

    @property
    def days_since(self) -> int:
        """The number of days since this sale."""
        return (utcnow() - self.timestamp).days


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
