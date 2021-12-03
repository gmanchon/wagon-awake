
import asyncio


async def main():

    print("hello")

    await sleep("bob")        # calls and wait for subroutine

    task = asyncio.create_task(sleep("bill"))

    # await task              # if await is not called the code does not wait for the completion of the task

    await asyncio.sleep(2)    # if we wait longer the task can complete even though not awaited

    print("done")


async def sleep(text):

    await asyncio.sleep(1)    # asyncio.sleep returns a coroutine

    print(text)


asyncio.run(main())           # executing main returns a coroutine because of the async keyword
