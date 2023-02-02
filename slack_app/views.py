from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import requests
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from slack import WebClient
from slack.errors import SlackApiError

from config.settings import SLACK_CLIENT_ID, SLACK_CLIENT_SECRET, SLACK_BOT_USER_TOKEN, SLACK_VERIFICATION_TOKEN
from .models import ClearHistoryModel


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "client_id": SLACK_CLIENT_ID
    }
    return render(request, 'slack/index.html', context)


def oauth(request: HttpRequest) -> HttpResponse:
    """
    botをワークスペースにインストールする

    == Send Request ==
    requests.get(url, {
        "code": "xxx",
        "client_id": "xxx",
        "client_secret": "xxx"
    })

    == Response ==
    {
        'ok': True,
        'access_token':
        'xoxp-xxx',
        'scope': 'xxx, yyy',
        'user_id': 'xxx',
        'team_id': 'xxx',
        'enterprise_id': None,
        'team_name': 'xxx',
        'bot': {
            'bot_user_id': 'xxx',
            'bot_access_token': 'xxx'
        }
    }
    """
    response = json.loads(
        requests.get('https://slack.com/api/oauth.access', params={
            "code": request.GET.get('code'),
            "client_id": SLACK_CLIENT_ID,
            "client_secret": SLACK_CLIENT_SECRET
        }).text
    )

    if response['ok']:
        return HttpResponse('ボットがワークスペースに参加しました！')
    else:
        return HttpResponse('失敗しました！リトライしてね！')


client = WebClient(token=SLACK_BOT_USER_TOKEN)


class Events(APIView):

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        # トークン認証
        if request.data.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Endpoint 認証
        if request.data.get('type') == 'url_verification':
            return Response(
                data=request.data,
                status=status.HTTP_200_OK
            )

        # Botのメッセージは除外する
        if request.data['event'].get('bot_id') is not None:
            print("Skipped bot message ...")
            return Response(status=status.HTTP_200_OK)

        # ⇓ ロジック ⇓
        message_info = request.data.get('event')

        channel = message_info.get('channel')
        user = message_info.get('user')
        text = message_info.get('text')

        clear_list = ['おふろチャレンジ成功', 'お風呂チャレンジ成功']

        if text in clear_list:
            # おふろチャレンジ成功
            try:
                client.chat_postMessage(
                    channel=channel,
                    text="えらい！！！"
                )
                record = ClearHistoryModel(user=user)
                record.save()
            except SlackApiError as e:
                print(e)
                return Response("Failed")

            return Response(status=status.HTTP_200_OK)
        if text == 'おふろチャレンジ失敗':
            try:
                client.chat_postMessage(
                    channel=channel,
                    text="にゃーん...😿"
                )
            except SlackApiError as e:
                print(e)
                return Response("Failed")

            return Response(status=status.HTTP_200_OK)
        if text == 'おふろチャレンジ記録':
            try:
                record = ClearHistoryModel.objects.filter(user=user).count()
                client.chat_postMessage(
                    channel=channel,
                    text=f"おふろチャレンジの記録は{record}回です！"
                )
            except SlackApiError as e:
                print(e)
                return Response("Failed")

        return Response(status=status.HTTP_200_OK)
