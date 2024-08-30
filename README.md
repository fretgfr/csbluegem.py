An asynchronous wrapper for the [CSBlueGem](https://csbluegem.com) API.

# Quickstart

```py
import asyncio
from textwrap import dedent

import csbluegem


async def main():
    async with csbluegem.Client() as client:
        results = await client.search("Bayonet")

        for result in results:
            s = f"""
                Pattern: {result.pattern}
                Float: {result.float}
                Stattrak?: {result.is_stattrak}
                Price: {result.price:,}
                Date: {result.timestamp}
                Origin: {result.origin}
                Days Since Sale: {result.days_since:,}
                """

            print(dedent(s), end="\n\n")


if __name__ == "__main__":
    asyncio.run(main())
```

Additional examples available [HERE](https://github.com/fretgfr/csbluegem.py/tree/master/examples)

Documentation available [HERE](https://csbluegempy.readthedocs.io/en/latest/)
