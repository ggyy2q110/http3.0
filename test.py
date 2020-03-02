"""
测试程序
"""
from socket import *
from config import *
import json

sock_tcp = socket()
sock_tcp.bind((frame_ip, frame_port))
sock_tcp.listen(5)

conn_tcp, addr = sock_tcp.accept()
data = conn_tcp.recv(1024 * 1024 * 10)
msg = json.loads(data)
print(msg)

data = {"status": "200", "data": "OK"}

msg = json.dumps(data)
conn_tcp.send(msg.encode())
