"""
模拟后端程序
"""
from socket import *
import json
from threading import Thread
from setting import *

ADDR = (Host, Port)


# 讲功能封装成类
class Application:
    def __init__(self):
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
    def start(self):
        self.sock_tcp.listen(5)
        print("Listen the port %d" % self.port)
        while True:
            conn_tcp, addr = self.sock_tcp.accept()
            print("Connect from", addr)
            t = Thread(target=self.handle, args=(conn_tcp,))
            t.setDaemon(True)
            t.start()

    # 出来来自http的请求
    def handle(self, conn_tcp):
        request = conn_tcp.recv(1024).decode()
        request = json.loads(request)  # {"method":"GET","info":"/"}
        # 分情况处理请求
        if request["method"] == "GET":
            if request["info"] == "/" or request["info"][-5:] == ".html":
                response = self.get_html(request["info"])
            else:
                # 请求非网页内容
                response = {"status": "404", "data": "xxxxxx"}

        elif request["method"] == "POST":
            pass
        # 讲数据返回给httpserver
        response = json.dumps(response)
        conn_tcp.send(response.encode())
        conn_tcp.close()

    def get_html(self, info):
        if info == "/":
            info = "index.html"
        try:
            f = open(dir + info)
        except:
            f = open(dir + "404.html")
            data = f.read()
            return {"status": "404", "data": data}

        # 返回网页内容
        data = f.read()
        return {"status": "200", "data": data}


app = Application()
app.start()
