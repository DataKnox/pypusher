import json
import requests


def pusher(user_key, api_token):
    push_url = "https://api.pushover.net/1/messages.json"
    payload = {"token": api_token,
               "user": user_key,
               "message": "hello world"}
    r = requests.post(url=push_url, data=payload)
    return r
