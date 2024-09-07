import asyncio
from textwrap import dedent

from csbluegem import BlueGemItem, Client


async def main():
    async with Client() as client:
        pdr = await client.pattern_data(BlueGemItem.GutKnife)

        for pd in pdr.pattern_data:
            s = f"""
                ### Playside Information
                Pattern: {pd.pattern}
                Playside Blue: {pd.playside_blue}
                Playside Purple: {pd.playside_purple}
                Playside Gold: {pd.playside_gold}
                Playside Blue Regions: {pd.playside_contour_blue}
                Playside Purple Regions: {pd.playside_contour_purple}
                """

            print(dedent(s), end="\n\n")


if __name__ == "__main__":
    asyncio.run(main())
