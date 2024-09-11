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
from typing import TYPE_CHECKING, Dict, Optional, Sequence, Type, Union

import aiohttp

from .errors import BadArgument
from .http import HTTPClient, Route
from .types import (
    Item,
    Currency,
    Filter,
    ItemType,
    Order,
    Origin,
    PatternDataResponse,
    Sale,
    SearchMeta,
    SearchResponse,
    SortKey,
)
from .utils import is_valid_pattern, is_valid_wear

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
        skin: Item,
        /,
        currency: Currency = Currency.USD,
        type: Optional[ItemType] = None,
        pattern: Optional[int] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        wear_min: Optional[float] = None,
        wear_max: Optional[float] = None,
        sort: SortKey = SortKey.Date,
        order: Order = Order.Desc,
        origin: Optional[Origin] = None,
        date_min: Optional[datetime.datetime] = None,
        date_max: Optional[datetime.datetime] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        pattern_data: bool = False,
        filters: Optional[Sequence[Filter]] = None,
    ) -> SearchResponse:
        """|coro|

        Searches for an item on CSBlueGem.

        Parameters
        ----------
        item: :class:`~csbluegem.types.Item`
            The item to search for.
        currency: :class:`~csbluegem.types.Currency`, optional
            The currency to return, by default USD.
        type: Optional[:class:`~csbluegem.types.ItemType`], optional
            The item's type, None for any. By default None.
        pattern: Optional[:class:`int`], optional
            The items pattern. None for any pattern. By default None.
        price_min: Optional[:class:`float`], optional
            The minimum price of the sale.
        price_max: Optional[:class:`float`], optional
            The maximum price of the sale.
        wear_min: Optional[:class:`float`], optional
            The minimum float of a returned item.
        wear_max: Optional[:class:`float`], optional
            The maximum float of a returned item.
        sort: :class:`~csbluegem.types.SortKey`, optional
            How should the results be sorted, by default Date.
        order: :class:`~csbluegem.types.Order`, optional
            How to order the results, by default DESC.
        origin: Optional[:class:`~csbluegem.types.Origin`], optional
            Where the sales originated from, None for any. By default None.
        date_min: Optional[:class:`datetime.datetime`], optional
            The earliest a sale can be from, None for no minimum, by default None.
        date_max: Optional[:class:`datetime.datetime`], optional
            The latest a sale can be from, None for no maximum, by default None.
        limit: Optional[:class:`int`], optional
            The maximum number of results to return. None for no limit. By default None.
        offset: Optional[:class:`int`], optional
            The offset to start returning results from. None for no offset. By default None.
        pattern_data: :class:`bool`, optional
            Whether to include pattern data in the returned results, by default False
        filters: :class:`~csbluegem.types.Filter`
            Filters to apply to the search.

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
        params: Dict[str, Union[str, float, int]] = {
            "skin": skin.value,
            "currency": currency.value,
            "sort": sort.value,
            "order": order.value,
        }

        if type is not None:
            params["type"] = type.value

        if pattern is not None:
            if not is_valid_pattern(pattern):
                raise BadArgument("pattern is invalid.")

            params["pattern"] = pattern

        if price_min is not None:
            params["price_min"] = price_min

        if price_max is not None:
            params["price_max"] = price_max

        if wear_min is not None:
            if not is_valid_wear(wear_min):
                raise BadArgument("float_min is not in range.")

            params["wear_min"] = wear_min

        if wear_max is not None:
            if not is_valid_wear(wear_max):
                raise BadArgument("float_max is not in range.")

            params["wear_max"] = wear_max

        if origin is not None:
            params["origin"] = origin.value

        if date_min is not None:
            params["date_min"] = int(date_min.timestamp())

        if date_max is not None:
            params["date_max"] = int(date_max.timestamp())

        if limit is not None:
            params["limit"] = limit

        if offset is not None:
            params["offset"] = offset

        if pattern_data is True:
            params["pattern_data"] = "true"

        if filters:
            for filter in filters:
                if not filter._is_valid():
                    raise BadArgument(f"a provided filter is invalid: {filter!r}")

                params[f"{filter.type.value}_min"] = filter.min
                params[f"{filter.type}_max"] = filter.max

        r = Route("GET", "/search")
        data = await self.http.request(r, params=params)

        return SearchResponse(SearchMeta._from_data(data["meta"]), [Sale._from_data(d) for d in data["sales"]])

    async def pattern_data(
        self,
        item: Item,
        /,
        pattern: Optional[int] = None,
        sort: SortKey = SortKey.Pattern,
        order: Order = Order.Desc,
        quantity: bool = False,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        filters: Optional[Sequence[Filter]] = None,
    ) -> PatternDataResponse:
        """|coro|

        Get pattern data for a skin.

        Parameters
        ----------
        item: :class:`~csbluegem.types.Item`
            The item to get pattern data for.
        pattern: Optional[:class:`int`], optional
            The pattern to get data for, None for any. By default None
        sort: :class:`~csbluegem.types.SortKey`, optional
            How the results should be sorted, by default pattern.
        order: :class:`~csbluegem.types.Order`, optional
            How to order the results, by default descending.
        quantity: :class:`bool`, optional
            Whether to return quantities of sales. By default False.
        offset: Optional[:class:`int`], optional
            The offset to start returning results from. None for no offset. By default None.
        limit: Optional[:class:`int`], optional
            The maximum number of results to return, None for no limit. By default None.

        Returns
        -------
        List[:class:`~csbluegem.types.PatternData`]
            The resulting data about the patterns.

        Raises
        ------
        :class:`~csbluegem.errors.BadArgument`
            You provided an invalid parameter.
        :class:`~csbluegem.errors.InvalidRequest`
            One of the parameters given was invalid.
        :class:`~csbluegem.errors.ServerError`
            The CSBlueGem server could not process the request.
        :class:`~csbluegem.errors.NotFound`
            The search returned no results.
        """
        params: Dict[str, Union[int, float, str]] = {
            "skin": item.value,
            "sort": sort.value,
            "order": order.value,
        }

        if pattern is not None:
            params["pattern"] = pattern

        if quantity is True:
            params["quantity"] = "true"

        if offset is not None:
            params["offset"] = offset

        if limit is not None:
            params["limit"] = limit

        if filters is not None:
            for filter in filters:
                if not filter._is_valid():
                    raise BadArgument(f"a provided filter is invalid: {filter!r}")

                params[f"{filter.type.value}_min"] = filter.min
                params[f"{filter.type}_max"] = filter.max

        r = Route("GET", "/patterndata")
        data = await self.http.request(r, params=params)

        return PatternDataResponse._from_data(data)

    async def pricecheck(self, item: Item, pattern: int, wear: float) -> int:
        """|coro|

        Runs a price check for an item.

        Parameters
        ----------
        item: :class:`~csbluegem.types.Item`
            The item to price check.
        pattern: :class:`int`
            The pattern of the item.
        wear: :class:`float`
            The float of the item

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
        if not is_valid_pattern(pattern):
            raise BadArgument("price check pattern must be 0 <= N <= 1000")

        if not is_valid_wear(wear):
            raise BadArgument("provided float is invalid.")

        params = {
            "skin": item.value,
            "pattern": pattern,
            "wear": wear,
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
