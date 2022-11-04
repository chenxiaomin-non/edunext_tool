import base64
import json

headers = {
    'authority': 'fuapi.edunext.vn',
    'accept': '*/*',
    'accept-language': 'en',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://fu.edunext.vn',
    'referer': 'https://fu.edunext.vn/',
    'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26',
}

user_information = {

}

group_mate = []

group_mate_dict = {}

def get_token():
    global user_information, headers
    data = ''

    if headers.get('authorization', None) == None:
        with open(".token", "r") as fh:
            data = fh.read()
        headers['authorization'] = data

    if user_information.get('UserId', None) == None:
        user_jwt = data.replace('Bearer ', '').split('.')[1].encode('utf-8')
        user_jwt = base64.b64decode(user_jwt + b'==').decode('utf-8')
        user_jwt = json.loads(user_jwt)
        user_information = {
            'UserId' : user_jwt['Id'],
            'UserName' : user_jwt['UserName'],
            'FullName' : user_jwt['FullName'],
        }
    return data
