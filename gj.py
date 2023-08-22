import asyncio
import websockets
import subprocess

def get_windows_system_uptime():
    try:
        output = subprocess.check_output("systeminfo | findstr /C:'System Boot Time'", shell=True)
        boot_time_str = output.decode("utf-8").strip().split(":")[1].strip()
        boot_time = " ".join(boot_time_str.split()[1:])
        return boot_time
    except Exception as e:
        print("获取系统启动时间失败:", e)
        return None

uptime = get_windows_system_uptime()
if uptime:
    print("系统启动时间:", uptime)

'''# WebSocket服务器的处理函数
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