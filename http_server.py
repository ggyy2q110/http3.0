"""
主程序
http server
"""
from socket import *
from config import *
from threading import Thread
import sys, time, re, json

# 服务器地址
ADDR = (Host, Port)


# 处理和webframe交互
def connect_frame(env):
    # 创建客户端套接字
    sock_tcp = socket()
    sock_tcp.connect((frame_ip, frame_port))

    try:
        # 将请求字典转化为json发送
        data = json.dumps(env)
        sock_tcp.send(data.encode())
        # 等待服务端返回数据
        data = sock_tcp.recv(1024 * 1024 * 10).decode()
        return json.loads(data)  # 转换为字典返回给主程序
    except:
        return


# 主程序与浏览器交互(负责解析http协议)
class HTTPServer:
    def __init__(self):
        # super().__init__()
        self.address = ADDR
        self.create_socket()
        self.bind()

    # 创建套接字
    def create_socket(self):
        # 与浏览器通信
        self.sock_tcp = socket()
        self.sock_tcp.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)

    def bind(self):
        self.sock_tcp.bind(self.address)
        self.host = self.address[0]
        self.port = self.address[1]

    # 搭建并发服务
    def server_forever(self):
        self.sock_tcp.listen(5)
        print("Listen the port %d" % self.port)
        while True:
            conn_tcp, addr = self.sock_tcp.accept()
            print("Connect from", addr)
            t = Thread(target=self.handle, args=(conn_tcp,))
            t.setDaemon(True)
            t.start()

    # 具体处理
    def handle(self, conn_tcp):
        request = conn_tcp.recv(4096).decode()
        pattern = r"(?P<method>[A-Z]+)\s+(?P<info>/\S*)"
        try:
            env = re.match(pattern, request).groupdict()
        except:
            conn_tcp.close()
            return
        else:
            data = connect_frame(env)
            if data:
                # data ==> {'status':'200','data':'xxxxxx'}
                self.response(conn_tcp, data)

    # 组织给浏览器的响应格式
    def response(self, conn_tcp, data):
        if data["status"] == "200":
            res = "HTTP/1.1 200 OK\r\n"
            res += "Content-Type:text/html\r\n"
            res += "\r\n"
            res += data["data"]
        elif data["status"] == "404":
            res = "HTTP/1.1 404 Not Found\r\n"
            res += "Content-Type:text/html\r\n"
            res += "\r\n"
            res += data["data"]
        elif data["status"] == "500":
            pass
        conn_tcp.send(res.encode())  # 发送给浏览器


httpd = HTTPServer()
httpd.server_forever()
