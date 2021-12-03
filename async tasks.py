
import asyncio


async def fetch_data():
    print("fetch data")
    await asyncio.sleep(2)
    print("got data")
    return {"data": 1}


async def print_numbers():
    for i in range(100):
        print(i)
        await asyncio.sleep(0.25)


async def main():
    task1 = asyncio.create_task(fetch_data())
    task2 = asyncio.create_task(print_numbers())

    data = await task1  #  ensure that task finishes and retrieve return value


asyncio.run(main())
