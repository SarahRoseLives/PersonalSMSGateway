from kivymd.app import MDApp
from kivy.lang import Builder
import socket
import json
from plyer import sms
from threading import Thread

KV = '''
BoxLayout:
    orientation: 'vertical'
    spacing: dp(20)
    padding: dp(20)
    pos_hint: {'center_x': 0.5, 'center_y': 0.5}

    Label:
        id: ip_label
        text: "Server running at: " + app.get_server_url()
        size_hint: None, None
        height: dp(50)
        pos_hint: {'center_x': 0.5}
        color: 0, 0, 0, 1

    Widget:
'''

class SMSGateway(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.socket_thread = None
        self.socket_running = False

    def get_local_ip(self):
        ip = 'N/A'
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0)
            s.connect(('10.254.254.254', 1))
            ip = s.getsockname()[0]
            s.close()
        except:
            pass
        return ip

    def get_server_url(self):
        return f"http://{self.get_local_ip()}:5000"

    def build(self):
        self.theme_cls.theme_style = "Light"  # Set theme to Light
        self.theme_cls.primary_palette = "BlueGray"
        self.start_socket_server()  # Start socket server on app launch
        return Builder.load_string(KV)

    def start_socket_server(self):
        self.socket_running = True

        def socket_thread():
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.get_local_ip(), 5000))
            server_socket.listen(5)
            print(f"Listening for connections on {self.get_local_ip()}:5000")

            while self.socket_running:
                client_socket, addr = server_socket.accept()
                print(f"Connection from {addr}")

                data = client_socket.recv(1024)
                if data:
                    message = json.loads(data.decode('utf-8'))
                    to_number = message.get('to_number')
                    message_body = message.get('message_body')

                    if not to_number or not message_body:
                        client_socket.sendall(json.dumps({'status': 'failed', 'reason': 'Recipient number or message body is missing'}).encode('utf-8'))
                    else:
                        # Send SMS using Plyer
                        sms.send(recipient=to_number, message=message_body)
                        client_socket.sendall(json.dumps({'status': 'success', 'recipient': to_number, 'message': message_body}).encode('utf-8'))

                client_socket.close()

        self.socket_thread = Thread(target=socket_thread)
        self.socket_thread.daemon = True
        self.socket_thread.start()

if __name__ == '__main__':
    SMSGateway().run()
