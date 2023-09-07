import json
import os
import re
import concurrent.futures
from pathlib import Path

import requests
from rest_framework_simplejwt.authentication import JWTAuthentication

from . import convert_operator
from .GPT_options import get_result
from .models import CompareList, Obj, Result
from rest_framework import serializers
from ast import literal_eval


BASE_DIR = Path(__file__).resolve().parent.parent


class ObjSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obj
        fields = ['object_name', 'images', 'thumbnail', 'object_url', 'obj_info', "comments"]

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['result_json']


# class CompareListSerializer(serializers.ModelSerializer):
#     objs = ObjSerializer(many=True, read_only=True)
#     result = ResultSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = CompareList
#         fields = ['created_at', 'id', 'objs', 'result']
#
#
#     def create(self, validated_data):
#         start = time.time()
#         user = self.context['request'].user
#
#         comparelist = CompareList.objects.create(user=user)
#
#         objs = self.context['request'].data
#         count = 0
#         for img_item, comment_item, object_name, thumbnail, object_url in zip(objs['images'].items(),
#                                                             objs['comments'].items(),
#                                                             objs['object_name'],
#                                                             objs['thumbnail'],
#                                                             objs['object_url']):
#             Obj.objects.create(comparelist=comparelist,
#                                images=img_item[1],
#                                comments=comment_item[1],
#                                object_name=object_name,
#                                thumbnail=thumbnail,
#                                object_url=object_url)
#
#
#             obj_info = {'object_name': object_name, 'img_text':[], 'comments':[]}
#
#
#             for url, comment in zip(img_item[1], comment_item[1]):
#                 directory = f'./information_images/comparelist_{comparelist.id}/{img_item[0]}/'
#                 count += 1
#                 download_file = requests.get(url)
#
#                 if not os.path.exists(directory):
#                     os.makedirs(directory)
#
#                 filename = f"{count}.jpg"
#
#                 file_path = os.path.join(directory, filename)
#
#                 with open(file_path, 'wb') as f:
#                     f.write(download_file.content)
#
#                 operate_path = os.path.abspath(file_path)
#                 text_chunk = convert_operator.get_text(operate_path, comparelist.id, img_item[0])
#                 obj_info['img_text'].extend(text_chunk)
#                 obj_info['comments'].append(comment)
#
#
#             print(obj_info)
#
#             # 받은 결과 반환
#
#
#         Result.objects.create(comparelist=comparelist)
#         end = time.time()
#         print(f"총 시간: {end-start:.4f} sec")
#         return comparelist


# 낙찰!!!

class CompareListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompareList
        fields = ['created_at', 'id',]
    def create(self, validated_data):
        # jwt_auth = JWTAuthentication()
        # user, _ = jwt_auth.authenticate(self.context['request'].user)
        # print(user)
        # print("성공")
        # print(self.context['request'].user)
        # print("tjdrhd")
        print(self.context['request'].user)
        user = self.context['request'].user
        objs = self.context['request'].data
        img_items = list(objs['images'].items())  # Convert dict_items to a list of tuples
        info_items = list(objs['obj_info'].items())
        comments = list(objs['comments'].items())
        object_names = objs['object_name']
        # print(img_items)
        for item in img_items:
            if item[1][0] == -1:
                item[1][0] = "https://gnu.kilho.net/data/file/qna/991097576_uFy5iwqK_3ef9ab5fb42640f19551c2e0dd4c36e3afd7ecfa.jpg"
        aspects = objs['aspects']
        # comparelist = CompareList.objects.create(aspects=aspects)
        comparelist = CompareList.objects.create(user=user, aspects=aspects)
        obj_list = []
        def download_image(url, file_path):
            download_file = requests.get(url)
            with open(file_path, 'wb') as f:
                f.write(download_file.content)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for index, (img_key, img_item) in enumerate(img_items):
                info_key, info_item = info_items[index]
                # print("이거")
                # print(comments[index])
                comment_key, comment_item = comments[index]
                object_name = object_names[index]
                thumbnail = objs['thumbnail'][index]
                object_url = objs['object_url'][index]
                obj = Obj(
                    comparelist=comparelist,
                    images=img_item,
                    obj_info=info_item,
                    object_name=object_name,
                    thumbnail=thumbnail,
                    object_url=object_url,
                    comments=comment_item
                )
                obj_list.append(obj)
                directory = f'./information_images/comparelist_{comparelist.id}/{img_key}/'
                if not os.path.exists(directory):
                    os.makedirs(directory)
                for count, (url, comment) in enumerate(zip(img_item, info_item), start=1):
                    filename = f"{count}.jpg"
                    file_path = os.path.join(directory, filename)
                    futures.append(executor.submit(download_image, url, file_path))
        product_json = {"products": []}
        # 이미지 다운로드가 완료된 후 처리 작업 시작
        for index, obj in enumerate(obj_list):
            directory = f'./information_images/comparelist_{comparelist.id}/{img_items[index][0]}/'
            img_text_list = []
            for count, (url, obj_info) in enumerate(zip(obj.images, obj.obj_info), start=1):
                filename = f"{count}.jpg"
                file_path = os.path.join(directory, filename)
                img_text_list.append(
                    convert_operator.get_text(os.path.abspath(file_path), comparelist.id, img_items[index][0]))
            object_name = obj.object_name
            img_text = "".join(sum(img_text_list, []))
            obj_info = obj.obj_info
            comment = obj.comments
            # print("댓글")
            # print(comment)
            obj_json = {
                "object_name": object_name,
                "img_text": img_text,
                "obj_info": obj_info,
                "comments": comment,
            }
            product_json["products"].append(obj_json)
            obj.img_text = img_text_list
            obj.save()
        # print(product_json)
        # print(aspects)
        # GPT 연결

        result_json = {}
        try:
            gpt_return = get_result(product_json, aspects)
            result = literal_eval(gpt_return)

            for idx, item in enumerate(result):
                result_json[f"res{idx+1}"] = item
                if str(type(item['selected_object_num'])) == "<class 'str'>":
                    # print("예외 발생")
                    item["selected_object_num"] = re.findall(r'\d', item["selected_object_num"])[0]
                    print(item["selected_object_num"])
                result_json[f"res{idx+1}"]["selected_obj_thumbnail"] = objs["thumbnail"][int(item["selected_object_num"])-1]
                result_json[f"res{idx+1}"]["selected_object_url"] = objs["object_url"][int(item["selected_object_num"]) - 1]
            if len(result_json) < len(aspects):
                length = len(result_json)
                for idx in range((len(aspects)-length)):
                    result_json[f"res{idx + length + 1}"] = "undefined"
        except Exception as e:
            result_json = {"ERROR": "ERROR, PLEASE TRY AGAIN."}
        Result.objects.create(comparelist=comparelist, result_json=result_json)
        return comparelist


class CompareListDetailSerializer(serializers.ModelSerializer):
    objs = ObjSerializer(many=True, read_only=True, source='obj_set')
    result = ResultSerializer(many=True, read_only=True, source='result_set')
    class Meta:
        model = CompareList
        fields = ['created_at', 'id', 'objs', 'result', 'aspects',]