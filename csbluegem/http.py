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

import json
from platform import python_version
from typing import Any, Dict, Literal, Optional, Union

import aiohttp

from .errors import HTTPException, InvalidRequest, NotFound, ServerError
from .meta import __version__

BASE_URL = "https://api.csbluegem.com/v2"
HTTP_METHOD = Literal["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "TRACE", "CONNECT", "OPTIONS"]


try:
    import orjson  # type: ignore
except ModuleNotFoundError:
    HAS_ORJSON = False
    loads = json.loads
    dumps = json.dumps
else:
    HAS_ORJSON = True
    loads = orjson.loads
    dumps = orjson.dumps


def from_json(string: str) -> Dict[Any, Any]:
    return loads(string)


def to_string(data: Dict[Any, Any]) -> str | bytes:
    return dumps(data)


class Route:
    """Represents a route for the API."""

    __slots__ = ("method", "path")

    def __init__(self, method: HTTP_METHOD, path: str) -> None:
        """An API route definition.

        Parameters
        ----------
        method: HTTP_METHOD
            The method the route requires.
        path: str
            The route's path.
        """
        self.method = method
        self.path = path


class HTTPClient:
    """Handles requests to the API, should not be used externally."""

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self.base_url = BASE_URL
        self.session: aiohttp.ClientSession = session or aiohttp.ClientSession()

        self.user_agent = f"csbluegem.py v{__version__} - Python-{python_version()} aiohttp-{aiohttp.__version__}"

    async def close(self) -> None:
        await self.session.close()

    async def _json_text_or_bytes(self, response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str, bytes]:
        content_type = response.headers.get("Content-Type")

        if content_type == "application/octet-stream":
            return await response.read()

        text = await response.text(encoding="utf-8")

        if content_type == "application/json":
            return from_json(text)

        return text

    async def request(self, route: Route, **kwargs: Any) -> Any:
        method = route.method
        url = f"{self.base_url}{route.path}"

        headers = {
            "User-Agent": self.user_agent,
        }

        if "json" in kwargs:
            headers["Content-Type"] = "application/json"

        async with self.session.request(method, url, headers=headers, **kwargs) as resp:
            status = resp.status

            data = await self._json_text_or_bytes(resp)

            if isinstance(data, dict):
                if (message := data.get("message")) is not None:
                    raise InvalidRequest(status, message)
            else:
                message = ""

            if status >= 500:
                raise ServerError(status, message or "")
            elif status == 404:
                raise NotFound(status, message or "")

            if 200 <= status < 300:
                return data

            raise HTTPException(status, f"an unexpected error occurred: {message}")
