import asyncio
import websockets

# WebSocket服务器的处理函数
async def echo(websocket, path):
    async for message in websocket:
        await websocket.send("收到消息：" + message)
        print("收到消息：" + message)

# 启动WebSocket服务器
start_server = websockets.serve(echo, "localhost", 8765)
# 运行事件循环
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
