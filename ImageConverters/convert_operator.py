import os
from pathlib import Path

import numpy as np
import platform
from PIL import ImageFont, ImageDraw, Image
from django.core.exceptions import ImproperlyConfigured
from matplotlib import pyplot as plt

import uuid
import json
import time
import cv2
import requests
import concurrent.futures


BASE_DIR = Path(__file__).resolve().parent.parent

secret_file = os.path.join(BASE_DIR, 'ocr_secret_key.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())



def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


secret_key = get_secret("secret_key")  # Your secret key here
api_url = get_secret("api_url")     # Your API URL here


def get_imagetext(path):
    path = path
    files = [('file', open(path,'rb'))]

    request_json = {'images': [{'format': 'jpg',
                                'name': 'demo'
                                }],
                    'requestId': str(uuid.uuid4()),
                    'version': 'V2',
                    'timestamp': int(round(time.time() * 1000))
                    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}

    headers = {
        'X-OCR-SECRET': secret_key,
    }

    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    result = response.json()

    text_box = []

    for field in result['images'][0]['fields']:
        text = field['inferText']
        text_box.append(text)

    return text_box


def process_image(path, comparelist_id, obj_id):
    img_size = Image.open(path).size

    if img_size[1] > 12000:
        # 이미지를 분할하여 각 부분에 대해 텍스트 추출
        if not os.path.exists(f'./long_path/comparelist_{comparelist_id}/{obj_id}/'):
            os.makedirs(f'./long_path/comparelist_{comparelist_id}/{obj_id}/')
        split_paths = []
        for i in range(2):
            size = (0, img_size[1] * i // 2, img_size[0], img_size[1] * (i + 1) // 2)
            crop_img = Image.open(path).crop(size)
            split_path = f'./long_path/comparelist_{comparelist_id}/{obj_id}/test{i + 1}.jpg'
            split_paths.append(split_path)
            crop_img.save(split_path)

        text_results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            text_results = list(executor.map(get_imagetext, split_paths))

        return [text for sublist in text_results for text in sublist]

    return get_imagetext(path)


def get_text(path, comparelist_id, obj_id):
    return process_image(path, comparelist_id, obj_id)


#

#
# from concurrent.futures import ProcessPoolExecutor
# import os
# from pathlib import Path
# from PIL import Image
# from django.core.exceptions import ImproperlyConfigured
# import uuid
# import json
# import time
# import requests
# from asgiref.sync import sync_to_async, async_to_sync
#
# import time
#
#
# # 병렬 처리를 위한 작업자 수
# NUM_WORKERS = 4
#
# BASE_DIR = Path(__file__).resolve().parent.parent
#
# secret_file = os.path.join(BASE_DIR, 'ocr_secret_key.json')
#
# with open(secret_file) as f:
#     secrets = json.loads(f.read())
#
# def get_secret(setting, secrets=secrets):
#     try:
#         return secrets[setting]
#     except KeyError:
#         error_msg = f"Set the {setting} environment variable"
#         raise ImproperlyConfigured(error_msg)
#
# secret_key = get_secret("secret_key")
# api_url = get_secret("api_url")
#
# async def process_images_parallel(split_paths):
#     start = time.time()
#     print("process_images_parallel 시작")
#     text_results = []
#     with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
#         text_results = list(executor.map(get_imagetext, split_paths))
#
#     end = time.time()
#     print("process_images_parallel 종료")
#     print(f"총 시간: {end-start:.4f} sec")
#     return text_results
#
# async def process_image_async(img, comparelist_id, obj_id):
#     img_size = img.size
#
#     if img_size[1] > 12000:
#         split_paths = []
#         for i in range(2):
#             size = (0, img_size[1] * i // 2, img_size[0], img_size[1] * (i + 1) // 2)
#             crop_img = img.crop(size)
#             split_path = os.path.abspath(f'./information_images/comparelist_{comparelist_id}/{obj_id}/test{i + 1}.jpg')
#             split_paths.append(split_path)
#             crop_img.save(split_path)
#
#         text_results = await process_images_parallel(split_paths)
#
#         return [text for sublist in text_results for text in sublist]
#
#     return get_imagetext_from_image(img)
#
# def get_imagetext_from_image(img):
#     start = time.time()
#     print("get_imagetext_from_image 시작")
#
#     img_path = os.path.abspath("./information_images/temp_image.png")
#     img.save(img_path, format="PNG")
#
#     end = time.time()
#
#     print("get_imagetext_from_image 종료")
#     print(f"총 시간: {end - start:.4f} sec")
#
#     return get_imagetext(img_path)
#
# def get_imagetext(path):
#     start = time.time()
#     print("get_imagetext 시작")
#     with open(path, 'rb') as f:
#         files = [('file', f)]
#
#         request_json = {
#             'images': [{'format': 'jpg', 'name': 'demo'}],
#             'requestId': str(uuid.uuid4()),
#             'version': 'V2',
#             'timestamp': int(round(time.time() * 1000))
#         }
#
#         payload = {'message': json.dumps(request_json).encode('UTF-8')}
#         headers = {'X-OCR-SECRET': secret_key}
#
#         response = requests.post(api_url, headers=headers, data=payload, files=files)
#         result = response.json()
#
#         text_box = [field['inferText'] for field in result['images'][0]['fields']]
#
#         end = time.time()
#
#         print("get_imagetext 종료")
#         print(f"총 시간: {end - start:.4f} sec")
#         return text_box
#
# @async_to_sync
# async def get_text(path, comparelist_id, obj_id):
#     img = Image.open(path)
#     return await process_image_async(img, comparelist_id, obj_id)
