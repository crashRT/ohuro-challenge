import websocket
import json
import os
from dotenv import load_dotenv
import re
import requests
from sqlalchemy.exc import SQLAlchemyError

from model import OhuroRecords, User

try:
    import thread
except ImportError:
    import _thread as thread
import time

load_dotenv()
USER_TOKEN = os.environ.get("USER_TOKEN")

OHURO = "(おふろ|お風呂)チャレンジ"

reaction_url = "https://misskey.crashrt.work/api/notes/reactions/create"
headers = {"Content-Type": "application/json"}


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
        print("##### message #####")
        print(loaded_message)
        print("##### end message #####")
        self.ohuro_challange(ws, loaded_message)

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
            "body": {"channel": "localTimeline", "id": "localTimelineId"},
        }
        self.ws.send(json.dumps(connect_data))

    def ohuro_challange(self, ws, message):
        body = message["body"]["body"]
        user = body["user"]
        print("user:", user)
        text = body["text"]
        print("text:", text)
        noteid = body["id"]
        print("noteid:", noteid)

        # にゃーん
        if re.compile("にゃーん").match(text):
            reaction_data = {
                "noteId": noteid,
                "reaction": "🐱",
                "i": USER_TOKEN,
            }
            r = requests.post(
                reaction_url, data=json.dumps(reaction_data), headers=headers
            )

        # おふろチャレンジ成功
        if re.compile(OHURO + "成功").match(text):
            # DB に記録
            record = OhuroRecords(user["username"])
            record.save_record()

            # リアクション
            reaction_data = {
                "noteId": noteid,
                "reaction": ":nyuuyokuhaigyo:",
                "i": USER_TOKEN,
            }
            r = requests.post(
                reaction_url, data=json.dumps(reaction_data), headers=headers
            )
            print("response:")
            print(r.status_code)
            print(r.headers)
            print(r.text)

        # ユーザー登録
        if re.compile(OHURO + "登録").match(text):
            # DBにユーザーを登録
            user = User(userid=user["id"], username=user["username"])
            user.save_user()

            # リアクション
            reaction_data = {
                "noteId": noteid,
                "reaction": ":ok_nya:",
                "i": USER_TOKEN,
            }
            r = requests.post(
                reaction_url, data=json.dumps(reaction_data), headers=headers
            )

        # 通知登録
        if re.compile(OHURO + "通知登録").match(text):
            try:
                user = User.get_user(user["userid"])
                user.subscribe_notify()
                self.react_ok(noteid)
            except SQLAlchemyError:
                # ユーザーが登録されていない場合
                user = User(userid=user["id"], username=user["username"], notify=True)
                user.save_user()
                self.react_ok(noteid)
            except:
                self.react_ng(noteid)

        # 通知解除
        if re.compile(OHURO + "通知解除").match(text):
            try:
                user = User.get_user(user["userid"])
                user.unsubscribe_notify()
            except SQLAlchemyError:
                # ユーザーが登録されていない場合
                user = User(userid=user["id"], username=user["username"], notify=False)
                user.save_user()

    def react_ok(self, noteid):
        reaction_data = {
            "noteId": noteid,
            "reaction": ":ok_nya:",
            "i": USER_TOKEN,
        }
        r = requests.post(reaction_url, data=json.dumps(reaction_data), headers=headers)

    def react_ng(self, noteid):
        reaction_data = {
            "noteId": noteid,
            "reaction": ":ng_nya:",
            "i": USER_TOKEN,
        }
        r = requests.post(reaction_url, data=json.dumps(reaction_data), headers=headers)


HOST_ADDR = "wss://misskey.crashrt.work/streaming?i={}".format(USER_TOKEN)
print(HOST_ADDR)
ws_client = Websocket_Client(HOST_ADDR)
ws_client.run_forever()
