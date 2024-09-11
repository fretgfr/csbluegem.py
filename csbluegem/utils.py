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
from itertools import islice
from typing import Any, Coroutine, Dict, Generator, Iterable, Optional, Tuple, TypeVar

__all__ = (
    "utcnow",
    "as_chunks",
    "safe_get",
)

T = TypeVar("T")
Coro = Coroutine[Any, Any, T]


def parse_date(date_string: str, /) -> datetime.datetime:
    """Returns an aware datetime denoting the date string given"""
    return datetime.datetime.strptime(date_string, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)


def parse_epoch(epoch: int, /) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(epoch, tz=datetime.timezone.utc)


def utcnow() -> datetime.datetime:
    """Returns an aware UTC datetime representing the current time.

    Returns
    --------
    :class:`datetime.datetime`
        The current aware datetime in UTC.
    """
    return datetime.datetime.now(datetime.timezone.utc)


# From the python docs for 3.12s `itertools.batched`
def as_chunks(iterable: Iterable[T], n: int) -> Generator[Tuple[T, ...], None, None]:
    """Batches an iterable into chunks of up to size n.

    Parameters
    ----------
    iterable : :class:`collections.abc.Iterable`
        The iterable to batch
    n : :class:`int`
        The number of elements per generated tuple.

    Raises
    ------
    :class:`ValueError`
        At least one result must be returned per group.
    """
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def safe_get(dict_: Dict[Any, Any], *keys: Any) -> Optional[Any]:
    """Safely get a nested key from a dictionary.

    ex.

    .. code-block:: python3

        d = {
            'i': 1,
            'j': {
                'k': '2'
            }
        }

        safe_get(d, 'i')  # -> 1
        safe_get(d, 'j', 'k')  # -> '2'


    Parameters
    ----------
    dict_ : Dict[Any, Any]
        The dictionary to get the key from
    keys : Any
        The keys to get from the dictionary. Processed in order.

    Returns
    -------
    Optional[Any]
        The value at the key. None if the key could not be gotten.
    """
    for key in keys:
        try:
            dict_ = dict_[key]
        except KeyError:
            return None

    return dict_


def is_valid_pattern(pattern: Optional[int]) -> bool:
    return 0 <= pattern <= 1000 if pattern is not None else True


def is_valid_wear(flt: float) -> bool:
    return 0.0000000000001 <= flt <= 1
