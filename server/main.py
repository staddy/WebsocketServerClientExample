import asyncio
import websockets


async def consumer_handler(websocket, path):
    try:
        async for message in websocket:
            print("received: ", message)
    except:
        pass


async def producer_handler(websocket, path):
    try:
        message = "server message"
        await websocket.send(message)
    except:
        pass


async def hello(websocket, path):
    print("new client")
    while True:
        consumer_task = asyncio.ensure_future(
            consumer_handler(websocket, path))
        producer_task = asyncio.ensure_future(
            producer_handler(websocket, path))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
        await asyncio.sleep(0.1)

start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
