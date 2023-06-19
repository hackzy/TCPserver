import random
import socket
from threading import Thread
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(('124.222.131.130',2164))
a = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n',\
            'o','p','q','r','s','t','u','v','w','x','y','z','y','x',\
            'a','b','a','b','a','b','a','b','s','b','a','b','a','b',\
                'w','u','v','g','h','j','k','l','m','p','q','e','r','t']


def xc():
    while True:
        账号 = random.choice(a) + random.choice(a) + random.choice(a) + str(random.randint(10000000000000000000000000,90000000000000000000000000)) + random.choice(a) + random.choice(a) + random.choice(a) 
        #密码 = random.choice(a) + random.choice(a) + random.choice(a) + str(random.randint(10000000000000000000000000,90000000000000000000000000)) + random.choice(a) + random.choice(a) + random.choice(a) 
        总 = bytes('ZC|' + 账号 + '|' + 账号,'gb2312')
        buffer = len(总).to_bytes(4,'little') + 总
        c.send(buffer)
        print(c.recv(1000).decode('gb2312'))

def th():
    t1 = Thread(target=xc)
    t1.start()
    t2 = Thread(target=xc)
    t2.start()
    t3 = Thread(target=xc)
    t3.start()
    t4 = Thread(target=xc)
    t4.start()

th()
