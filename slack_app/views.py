from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import requests
import json

from config.settings import SLACK_CLIENT_ID, SLACK_CLIENT_SECRET


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "client_id": SLACK_CLIENT_ID
    }
    return render(request, 'slack/index.html', context)


def oauth(request: HttpRequest) -> HttpResponse:
    """
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
