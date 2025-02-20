import asyncio
import websockets
import os
from src.plug.saveData import 存档

folder_path = './json'

存档.每日数据刷新()


'''for file in files:
        file_path = os.path.join(root, file)
        print(file_path)'''


'''
async def echo(websocket, path):
    async for message in websocket:
        await websocket.send("收到消息：" + message)
        print("收到消息：" + message)

# 启动WebSocket服务器
start_server = websockets.serve(echo, "localhost", 8765)
# 运行事件循环
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
'''