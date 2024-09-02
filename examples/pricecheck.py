import asyncio

import csbluegem


async def main():
    async with csbluegem.Client() as client:
        result = await client.pricecheck(csbluegem.BlueGemKnife.ClassicKnife, pattern=222, float=0.2430)

        print(result)


if __name__ == "__main__":
    asyncio.run(main())
