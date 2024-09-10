An asynchronous wrapper for the [CSBlueGem](https://csbluegem.com) API.

# Quickstart

Install from PyPI: `python3 -m pip install csbluegem.py`

```py
import asyncio
from textwrap import dedent

import csbluegem


async def main():
    async with csbluegem.Client() as client:
        r = await client.search(csbluegem.Item.M9Bayonet)

        for result in r.sales:
            s = f"""
                Pattern: {result.pattern}
                Float: {result.float}
                Stattrak?: {result.is_stattrak}
                Price: {result.price:,}
                Date: {result.timestamp}
                Origin: {result.origin.value}
                Days Since Sale: {result.days_since:,}
                """

            print(dedent(s), end="\n\n")


if __name__ == "__main__":
    asyncio.run(main())
```

Additional examples available [HERE](https://github.com/fretgfr/csbluegem.py/tree/master/examples)

Documentation available [HERE](https://csbluegempy.readthedocs.io/en/latest/)
