import json, requests

from model import OhuroRecords, Users
from app import USER_TOKEN, headers, note_create_url, reaction_url


def request_challange():
    """
    おふろチャレンジするよう通知する
    """
    print("おふろチャレンジを通知したよ！！！")
    users = Users.get_notify_users()
    if len(users) == 0:  ## 誰も登録していなかったらなにもしない
        return
    text = "おふろチャレンジ"
    for user in users:
        text = "@{} {}".format(user.username, text)
    note_data = {
        "i": USER_TOKEN,
        "text": text,
        "visibility": "specified",
        "visibleUserIds": [user.userid for user in users],
        "localOnly": False,
        "noExtractMentions": False,
        "noExtractHashtags": False,
        "noExtractEmojis": False,
    }
    r = requests.post(note_create_url, data=json.dumps(note_data), headers=headers)
