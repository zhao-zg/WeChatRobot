import json
from http.server import BaseHTTPRequestHandler, HTTPServer

robot = None

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/contacts':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(robot.allContacts).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    def do_POST(self):
        #if self.path == '/':
        content_length = int(self.headers['Content-Length'])  # 获取请求体的长度
        post_data = self.rfile.read(content_length)  # 读取请求体
        try:
            new_data = json.loads(post_data)  # 将请求体解析为JSON
            print(new_data)
            self.reply(new_data)
        except json.JSONDecodeError:
            self.send_response(400)  # 返回400错误
            self.end_headers()
        #else:
        #    self.send_response(404)
        #    self.end_headers()
    def reply(self, json_data):
        if robot == None:
            print("Not init robot")
            return
        match json_data["api"]:
            case "text":
                robot.sendTextMsg(json_data["msg"],json_data["receiver"])
                return
            case "image":
                return
            case "file":
                return
            case "AddIntoGroup":
                return
            case _:
                return

def run(wcfRobot=None):
    from configuration import Config
    config = Config().API_SERVER
    if not config:
        exit(0)
    global robot
    robot = wcfRobot
    server_address = ('', config.get('port'))  # 监听所有可用的地址
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting apiServer on port {config.get('port')}...')
    httpd.serve_forever()