import websocket
import json
import os
from dotenv import load_dotenv

try:
    import thread
except ImportError:
    import _thread as thread
import time

load_dotenv()
USER_TOKEN = os.environ.get("USER_TOKEN")


class Websocket_Client:
    def __init__(self, host_addr):
        # デバックログの表示/非表示設定
        websocket.enableTrace(True)

        # WebSocketAppクラスを生成
        # 関数登録のために、ラムダ式を使用
        self.ws = websocket.WebSocketApp(
            host_addr,
            on_message=lambda ws, msg: self.on_message(ws, msg),
            on_error=lambda ws, msg: self.on_error(ws, msg),
            on_close=lambda ws: self.on_close(ws),
        )
        self.ws.on_open = lambda ws: self.on_open(ws)

    # メッセージ受信に呼ばれる関数
    def on_message(self, ws, message):
        loaded_message = json.loads(message)
        print(loaded_message)

    # エラー時に呼ばれる関数
    def on_error(self, ws, error):
        print(error)

    # サーバーから切断時に呼ばれる関数
    def on_close(self, ws):
        print("### closed ###")

    # サーバーから接続時に呼ばれる関数
    def on_open(self, ws):
        thread.start_new_thread(self.run, ())

    # サーバーから接続時にスレッドで起動する関数
    def run(self, *args):
        self.connect_localTimeline()

    # websocketクライアント起動
    def run_forever(self):
        self.ws.run_forever()

    def connect_localTimeline(self):
        connect_data = {
            "type": "connect",
            "body": {"channel": "localTimeline", "id": "localTimeline"},
        }
        self.ws.send(json.dumps(connect_data))


HOST_ADDR = "wss://misskey.crashrt.work/streaming?i={}".format(USER_TOKEN)
print(HOST_ADDR)
ws_client = Websocket_Client(HOST_ADDR)
ws_client.run_forever()
