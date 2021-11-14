import requests
import json
import base64

# 别问，问就砍feature了没写完

api = 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/video_cls/diedaojiance'
app_id = ''
api_key = ''
secret_key = ''


# client_id为api key client_secret为secret key
def get_access_token(client_id, client_secret):
    url = 'https://aip.baidubce.com/oauth/2.0/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': api_key,
        'client_secret': client_secret
    }
    res = requests.post(url=url, data=data)
    print(res.json()['refresh_token'])
    return res.json()['refresh_token']


def send_video(access_token, video):
    url = api
    headers = {
        'Content-Type': 'application/json',
        'access_token': access_token
    }
    data = {
        'video': video,
        'top_num': 6
    }
    res = requests.post(url=url, headers=headers, data=data)
    print(res.json())


if __name__ == '__main__':
    video = ''
    access_token = get_access_token(api_key, secret_key)
    send_video(access_token, video)
