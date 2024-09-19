import asyncio
from textwrap import dedent

import csbluegem


async def main():
    async with csbluegem.Client() as client:
        r = await client.search(csbluegem.Item.FiveSeveN)

        for result in r.sales:
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
