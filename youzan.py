"""
有赞滑块验证码识别
~~~~~~~~~~~~~~~
usage:
   >>> import youzan

   >>> yz = youzan.YouZan()
   >>> yz.get_token()
   >>> yz.get_captcha()
   >>> solution = yz.check()
   >>> print(solution)

   {"code": 0, "msg": "ok", "data": {"captchaType": 1, "success": true, "token": "67999c5c782a3156639389937093d220"}}
"""


import json
import requests
import utils

class YouZan:
    def __init__(self):
        self.base_url = 'https://passport.youzan.com/'
        self.token = ''
        self.randomStr = ''
        self.captcha = {}
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }


    def get_token(self):
        url = self.base_url + 'api/captcha/get-behavior-captcha-token-v2.json?bizType=15&version=1.0'
        response = requests.get(url, headers=self.headers)
        utils.response_assert(response)
        jdata = response.json()
        self.token = jdata['data']['token']
        self.randomStr = jdata['data']['randomStr']


    def get_captcha(self):
        url = self.base_url + f'api/captcha/get-behavior-captcha-data.json?token={self.token}&captchaType=1'
        response = requests.get(url, headers=self.headers)
        utils.response_assert(response)
        jdata = response.json()
        self.captcha = jdata['data']['captchaObtainInfoResult']


    def check(self):
        point = utils.translate(self.captcha['bigUrl'], self.captcha['smallUrl'])
        userBehaviorData = utils.generate_sliding(point, self.captcha['cy'], self.randomStr)
        url = self.base_url + 'api/captcha/check-behavior-captcha-data.json'
        payload = {
            'token': self.token,
            'captchaType': '1',
            'userBehaviorData': userBehaviorData,
            'bizData': '',
            'bizType': '15'
        }
        response = requests.post(url, json=payload, headers=self.headers)
        utils.response_assert(response)
        jdata = response.json()
        assert jdata['data']['success'] is True, f'captcha check failed, error message is {jdata["msg"]}'
        jdata['data']['token'] = self.token
        return json.dumps(jdata)

