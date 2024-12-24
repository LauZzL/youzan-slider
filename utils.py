import json
import random
import time

import ddddocr
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

det = ddddocr.DdddOcr(det=False, ocr=False)


def translate(bg, slide):
    bg_byte = requests.get(bg).content
    slide_byte = requests.get(slide).content
    res = det.slide_match(slide_byte, bg_byte)
    # scale = 0.5
    return int(res['target'][0] * 0.5) - 6


def encrypt(randomStr, data):
    c = randomStr.split('@')
    key = ''.join(c[1][::-1])
    iv = ''.join(c[0][::-1])
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    padded_data = pad(data.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    return encoded_ciphertext



def sliding_event(end_x):
    mx = -1
    my = -1
    ts = -1
    timestamp = time.time()
    timestamp = int(timestamp * 1000)
    result = []
    start_x = random.randint(15, 40)
    start_y = random.randint(185, 225)

    for i in range(1, 3001):
        if i == 1:
            mx = start_x
            my = start_y
            ts = timestamp
        elif 1 < i <= 17:
            mx = 1
            my = random.choices([0] * 8 + [1], k=1)[0]
            ts = random.choices([0] * 8 + [1], k=1)[0]
            start_x += mx
        elif 17 < i <= 60:
            mx = random.randint(2, 8)
            my = random.choices([0] * 8 + [1], k=1)[0]
            ts = random.choices([0] * 8 + [1], k=1)[0]
            start_x += mx
        elif i > 60:
            mx = random.choice([1, 2])
            my = 0
            ts = random.choices([0] * 8 + [1], k=1)[0]
            start_x += mx

        json_obj = {"mx": mx, "my": my, "ts": ts}
        if start_x < end_x:
            result.append(json_obj)
        elif start_x == end_x:
            result.append(json_obj)
            break

    return result



def generate_sliding(end_x, cy, randomStr):
    scale = 0.5
    cy = int(cy * scale)
    slidingEvent = sliding_event(end_x)
    return encrypt(randomStr, json.dumps({
        "cx": end_x,
        "cy": cy,
        "scale": scale,
        "slidingEvents": slidingEvent
    }))




def response_assert(response):
    assert response.status_code == 200, f'response status code is {response.status_code}'
    assert response.headers['Content-Type'] == 'application/json; charset=utf-8', f'response content type is {response.headers["Content-Type"]}'
    assert response.json()['code'] == 0, f'response code is {response.json()["code"]}, error message is {response.json()["msg"]}'



