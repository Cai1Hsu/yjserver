"""
MIT License

Copyright (c) 2023 Cai1Hsu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
import socket
import json
import time
import argparse
import threading
import uuid
import random

from http.server import HTTPServer, BaseHTTPRequestHandler

"""
    IMPORTANT: YOU MUST CHANGE THESE VALUES
    YOU MUST OBTAIN THESE VALUES BY REVERSE ENGINNERING
"""
# HACKING VARIABLES
padpwd = "##########SENSITIVIE DATA##########"
user_code = "##########SENSITIVIE DATA##########"
user_name = "##########SENSITIVIE DATA##########"
user_gender = "##########SENSITIVIE DATA##########"
user_id = "##########SENSITIVIE DATA##########"
school_name = "##########SENSITIVIE DATA##########"
school_domain = "0.0.0.0"
school_domain_without_port = "0.0.0.0"
pubkey = "##########SENSITIVIE DATA##########"
privatekey = "##########SENSITIVIE DATA##########"
apk_file = "./launcher3.apk"

# global variables
g_server = None
g_server_port = 0
g_server_address = None
g_server_thread = None
g_server_shutdown = False
g_server_shutdown_lock = threading.Lock()

# global variables for the server
g_server_data = None
g_server_data_lock = threading.Lock()

# global hacking variables
onfig_payload = {
    "status": True,
    "errorNum": 0,
    "errorInfo": "",
    "data": {
        "user": {
            "id": user_id,
            "usercode": user_code,
            "usernumber": user_code,
            "name": user_name,
            "photo": "",
            "gender": user_gender,
            "pubkey": pubkey,
            "type": "03",
            "school": [
                {
                    "id": "1",
                    "name": school_name
                }
            ],
            "children": [],
            "isxiaozhang": 0,
            "showDict": -1
        },
        "privatekey": privatekey,
        "encrypt": "md5",
        "tigase": {
            "domain": school_domain_without_port,
            "port": "##########SENSITIVIE DATA##########",
            "ip": "##########SENSITIVIE DATA##########"
        },
        "mongo": {
            "domain": school_domain_without_port,
            "port": "##########SENSITIVIE DATA##########",
            "user": "##########SENSITIVIE DATA##########",
            "pwd": "##########SENSITIVIE DATA##########"
        },
        "cloud": [],
        "acs": [],
        "apihost": school_domain,
        "questiontype": [
            "\u5355\u9009\u9898",
            "\u591a\u9009\u9898",
            "\u5224\u65ad\u9898",
            "\u586b\u7a7a\u9898",
            "\u8ba1\u7b97\u9898",
            "\u7b80\u7b54\u9898"
        ],
        "guidelearncomment": 0,
        "guidenotes": 0,
        "lesson": {
            "comment": 0,
            "notes": 0,
            "favorite": 0,
            "answer": 0
        },
        "ebag": {
            "desktopicon": {
                "background": {
                    "small": "",
                    "normal": "",
                    "large": ""
                },
                "wifi": "##########SENSITIVIE DATA##########",
                "setting": "##########SENSITIVIE DATA##########",
                "batterycolor": "#12B0A9"
            },
            "app": [
                {
                    "code": "daoxueben",
                    "name": "\u5bfc\u5b66\u672c",
                    "color": "#000000",
                    "icon": "##########SENSITIVIE DATA##########",
                    "enable": 1,
                    "config": {
                        "download": 1,
                        "comment": 1
                    }
                },
                {
                    "code": "zuoyefudao",
                    "name": "\u4f5c\u4e1a\u8f85\u5bfc",
                    "color": "#000000",
                    "icon": "##########SENSITIVIE DATA##########",
                    "enable": 1,
                    "config": []
                },
                {
                    "code": "myhomework",
                    "name": "\u6211\u7684\u4f5c\u4e1a",
                    "color": "#000000",
                    "icon": "##########SENSITIVIE DATA##########",
                    "enable": 1,
                    "config": []
                },
                {
                    "code": "cuotiji",
                    "name": "\u9519\u9898\u96c6",
                    "color": "#000000",
                    "icon": "##########SENSITIVIE DATA##########",
                    "enable": 1,
                    "config": []
                },
                {
                    "code": "afd_mybook",
                    "name": "\u6211\u7684\u8bfe\u672c",
                    "color": "#000000",
                    "icon": "##########SENSITIVIE DATA##########",
                    "enable": 1,
                    "config": []
                },
                {
                    "code": "my_app",
                    "name": "\u6211\u7684\u5e94\u7528",
                    "color": "#000000",
                    "icon": "##########SENSITIVIE DATA##########",
                    "enable": 1,
                    "config": []
                },
                {
                    "code": "hudongtaolun",
                    "name": "\u4e92\u52a8\u8ba8\u8bba",
                    "color": "#000000",
                    "icon": "##########SENSITIVIE DATA##########",
                    "enable": 1,
                    "config": []
                },
                {
                    "code": "study_store",
                    "name": "\u5b66\u4e60\u5546\u5e97",
                    "color": "#000000",
                    "icon": "##########SENSITIVIE DATA##########",
                    "enable": 1,
                    "config": []
                },
                {
                    "code": "happ_class",
                    "name": "\u667a\u6167\u8bfe\u5802",
                    "color": "#000000",
                    "icon": "##########SENSITIVIE DATA##########",
                    "enable": 1,
                    "config": []
                }
            ],
            "updatetime": 1606379332
        },
        "schoolmsg": "0",
        "qbVer": "v3"
    }
}

padpwd_payload = {
    "status":True,
    "errorNum":0,
    "errorInfo":"",
    "data": padpwd
}

app_payload = {}

notification_payload = {
    "status": True,
    "errorNum": 200,
    "errorInfo": "",
    "data": {
        "Message": [
        ],
        "count": 0,
        "UserName": user_name,
        "UserCode": user_code
    }
}

# set up server
class Server(BaseHTTPRequestHandler):
    def do_GET_or_POST(self):
        # handle request
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Hello, world!')
        elif self.path.startswith('/download'):
            apk_path = self.path[self.path.lastindex('/') + 1:]
            # check if file exists
            if not os.path.exists(apk_path):
                self.send_error(404, 'File Not Found: %s' % self.path)
                return
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.send_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(apk_path))
            self.send_header('Content-Length', os.path.getsize(apk_path))
            self.end_headers()
            # send the apk file
            with open(apk_path, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    self.wfile.write(data)

        elif self.path.startswith('/api/config'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(dict_to_json(config_payload).encode('utf-8'))
        elif self.path.startswith('/api/padpwd'):
            # send config file
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(dict_to_json(padpwd_payload).encode('utf-8'))
        elif self.path.startswith('/api/app/projectcode/ebag/os/android'):
            # send config file
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(dict_to_json(app_payload).encode('utf-8'))
        elif self.path.startswith('/api/app/projectcode/myapp/os/android'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(dict_to_json(app_payload).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        self.do_GET_or_POST()

    def do_GET(self):
        self.do_GET_or_POST()

    def log_request(self, data):
        def get_device_type():
            if 'Android' in self.headers['User-Agent']:
                return 'Android'
            if 'Linux' in self.headers['User-Agent']:
                return 'Linux'
            if 'Windows' in self.headers['User-Agent']:
                return 'Windows'
            return 'Android'
        
        print('Reuqeseting(%s) %s by %s(%s) at %s' % (self.command,
                                              self.path, 
                                              self.client_address[0],
                                              get_device_type(),
                                              time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        # print formated header
        print('\thedaers:')
        for h in self.headers:
            print('\t\t%s: %s' % (h, self.headers[h]))
        
        print('', end='\n')

    def run_server():
        global g_server
        global g_server_port
        global g_server_address
        global g_server_thread
        global g_server_shutdown
        global g_server_shutdown_lock

        # create server
        g_server = HTTPServer((g_server_address, g_server_port), Server)
        # allow any access
        g_server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        g_server.server_bind = lambda self: self.socket.bind(self.server_address)
        g_server.server_activate = lambda self: self.socket.listen(self.request_queue_size)
        g_server.allow_reuse_address = True

        g_server_thread = threading.Thread(target=g_server.serve_forever)
        g_server_thread.start()

        # handle request
        while True:
            try:
                # check shutdown flag
                g_server_shutdown_lock.acquire()
                if g_server_shutdown:
                    g_server_shutdown_lock.release()
                    break
                g_server_shutdown_lock.release()

                # sleep for a while
                time.sleep(1)
            except KeyboardInterrupt:
                # set shutdown flag
                g_server_shutdown_lock.acquire()
                g_server_shutdown = True
                g_server_shutdown_lock.release()
                g_server.shutdown()
                g_server_thread.join()
                break

        # shutdown server
        g_server.shutdown()
        g_server_thread.join()

    def start_server(port, address):
        global g_server_port
        global g_server_address

        # set port and address
        g_server_port = port
        g_server_address = address

        # start server
        Server.run_server()

    def stop_server():
        global g_server_shutdown
        global g_server_shutdown_lock

        # set shutdown flag
        g_server_shutdown_lock.acquire()
        g_server_shutdown = True
        g_server_shutdown_lock.release()

def main():
    global apk_file
    global app_payload 
    global school_domain
    global school_domain_without_port

    # parse arguments
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--debug', action='store_true', help='debug mode')
    parser.add_argument('debug', action='store_true', help='debug mode')
    parser.add_argument('--port', type=int, default=8080, help='server port')
    parser.add_argument('--address', type=str, default='0.0.0.0', help='server address')
    args = parser.parse_args()

    port = args.port

    school_domain_without_port = get_inet_ip()
    school_domain = school_domain_without_port + ':' + str(port)
    app_payload = generate_app_payload()

    if school_domain == '127.0.0.1':
        print('You are not in school network, please connect to school network first.')

    # if args.debug:
    #     debug()
    #     return

    # print local access ip with port
    print('Server is running at http://%s:%d' % (args.address, args.port))

    # start server
    Server.start_server(args.port, args.address)

def dict_to_json(d):
    return json.dumps(d)

def generate_app_payload():
    global school_domain
    global apk_file
    
    name = str(uuid.uuid4()) + '.apk'
    ver = random.randint(1490, 2000)
    return {
        "status": True,
        "errorNum": 0,
        "errorInfo": "",
        ###########################################################
        # IMPORTANT : YOU MUST CHANGE THE VALUES TO YOUR OWN ONES #
        ###########################################################
        "data": [
            {
                "appname": name,
                # use this to keep apps from being removed
                "packagename": "com.launcher.activity",
                # trigger auto slient install 
                "versioncode": str(ver),
                # anything is ok
                "versionname": "8.4.90",
                "apptype": "",
                "apkname": name,
                "appsize": os.path.getsize(apk_file),
                "iconurl": "",
                "appwebpath": "http:\/\/" + school_domain + "\/download\/" + name,  
                "name": "Android"
            }
        ]
    }

def get_inet_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        ip = st.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        st.close()
    return ip


if __name__ == '__main__':
    main()

##################################
# ONE WAY TO BYPASS THE CHECKSUM #
##################################
"""
``` java
private boolean checkConfig(String jsonStr, String timeStamp2) {
    JSONObject json = new JSONObject(jsonStr);
    if (!json.has("checksum")) {
        return true;
    }
    JSONObject data = json.getJSONObject("data");
    String jSONObject = data.toString();
    String checksum = json.getString("checksum");
    String seed = data.getString("privatekey");
    String md5String = My_md5.Md5(AESUtils.encrypt(seed, String.valueOf(seed) + data.getString("apihost") + timeStamp2));
    if (md5String == null || checksum == null || !md5String.equals(checksum)) {
        return false;
    }
}
```
According to line 3, we can hack it by sending a json string without checksum field.
"""
