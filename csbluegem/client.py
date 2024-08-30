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
from types import TracebackType
from typing import TYPE_CHECKING, List, Optional, Type

import aiohttp

from .errors import BadArgument
from .http import HTTPClient, Route
from .types import BlueGemItem, BlueGemKnives, Currency, Filter, ItemType, Order, Origin, Sale, SortKey
from .utils import _is_valid_float, _is_valid_pricecheck_pattern, _is_valid_search_pattern, utcnow

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ("Client",)


class Client:
    """A CSBlueGem Client.

    .. container:: operations

        .. describe:: async with x:

            Returns the Client itself. Used to gracefully close the client on exit.

            .. code-block:: python3

                async with csbluegem.Client() as client:
                    ...
    """

    def __init__(self, session: Optional[aiohttp.ClientSession] = None) -> None:
        self.http = HTTPClient(session=session)

    async def search(
        self,
        skin: BlueGemItem,
        currency: Currency = "USD",
        type: ItemType = "any",
        pattern: int = -1,
        price_min: float = 0,
        price_max: float = 9999999999.99,
        float_min: float = 0,
        float_max: float = 1,
        sort_key: SortKey = "date",
        sort: Order = "descending",
        origin: Origin = "any",
        filter0: Filter = "playside_blue",
        filter0_min: int = 0,
        filter0_max: int = 999,
        date_min: Optional[datetime.datetime] = None,
        date_max: Optional[datetime.datetime] = None,
    ) -> List[Sale]:
        """Searches for an item on CSBlueGem.

        Parameters
        ----------
        skin: BlueGemItem
            The skin to search for.
        currency: Currency, optional
            The currency to return, by default "USD"
        type: ItemType, optional
            The item's type, by default "any"
        pattern: :class:`int`, optional
            The items pattern. -1 for any pattern, by default -1
        price_min: :class:`float`, optional
            The minimum price of the sale, by default 0
        price_max: :class:`float`, optional
            The maximum price of the sale, by default 9999999999.99
        float_min: :class:`float`, optional
            The minimum float of a returned item, by default 0
        float_max: :class:`float`, optional
            The maximum float of a returned item, by default 1
        sort_key: SortKey, optional
            How should the results be sorted, by default "date"
        sort: Order, optional
            How to order the results, by default "descending"
        origin: Origin, optional
            Where the sales originated from, by default "any"
        filter0: Filter, optional
            Additional filter criteria, by default "playside_blue"
        filter0_min: :class:`int`, optional
            Parameter for additional filter criteria, by default 0
        filter0_max: :class:`int`, optional
            Parameter for additional filter criteria, by default 999
        date_min: Optional[:class:`datetime.datetime`], optional
            The earliest a sale can be from, None for no minimum, by default None
        date_max: Optional[:class:`datetime.datetime`], optional
            The latest a sale can be from, None for no maximum, by default None

        Returns
        -------
        List[:class:`~csbluegem.types.Sale`]
            The returned sales.

        Raises
        -------
        :class:`~csbluegem.errors.BadArgument`
            You provided an invalid parameter.
        :class:`~csbluegem.errors.InvalidRequest`
            One of the parameters given was invalid.
        :class:`~csbluegem.errors.ServerError`
            The CSBlueGem server could not process the request.
        :class:`~csbluegem.errors.NotFound`
            The search returned no results.
        """
        if not (_is_valid_float(float_min) and _is_valid_float(float_max)):
            raise BadArgument("float is not in range.")

        if not _is_valid_search_pattern(pattern):
            raise BadArgument("pattern is invalid")

        params = {
            "skin": skin,
            "currency": currency,
            "type": type,
            "pattern": pattern,
            "price_min": price_min,
            "price_max": price_max,
            "float_min": float_min,
            "float_max": float_max,
            "sort_key": sort_key,
            "sort": sort,
            "origin": origin,
            "filter0": filter0,
            "filter0_min": filter0_min,
            "filter0_max": filter0_max,
        }

        if date_min is not None:
            params["date_min"] = date_min.timestamp()

        if date_max is not None:
            params["date_max"] = date_max.timestamp()

        r = Route("GET", "/search")
        data = await self.http.request(r, params=params)

        return [Sale._from_dict(d) for d in data]

    async def pricecheck(self, knife: BlueGemKnives, pattern: int, float: float) -> int:
        """Runs a price check for an item.

        Parameters
        ----------
        knife: BlueGemKnives
            The knife to price check.
        pattern: :class:`int`
            The pattern of the knife.
        float: :class:`float`
            The float of the knife

        Returns
        -------
        :class:`int`
            The price check value, in USD.

        Raises
        ------
        :class:`~csbluegem.errors.BadArgument`
            You provided an invalid argument.
        :class:`~csbluegem.errors.InvalidRequest`
            One of the parameters given was invalid.
        :class:`~csbluegem.errors.ServerError`
            The CSBlueGem server could not process the request.
        :class:`~csbluegem.errors.NotFound`
            The search returned no results.
        """
        if not _is_valid_pricecheck_pattern(pattern):
            raise BadArgument("price check pattern must be 0 <= N <= 1000")

        if not _is_valid_float(float):
            raise BadArgument("provided float is invalid.")

        params = {
            "skin": knife,
            "pattern": pattern,
            "float": float,
        }

        r = Route("GET", "/pricecheck")
        data = await self.http.request(r, params=params)

        return int(data)

    async def close(self) -> None:
        """Gracefully close the client."""
        await self.http.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        await self.close()
