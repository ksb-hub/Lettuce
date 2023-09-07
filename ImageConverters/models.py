from django.db import models

from accounts.models import User


class CompareList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    aspects = models.CharField(max_length=200, default=[1, 4])


class Obj(models.Model):
    comparelist = models.ForeignKey(CompareList, on_delete=models.CASCADE)
    object_name = models.CharField(max_length=100)
    images = models.JSONField(default='{}')
    obj_info = models.JSONField(default='{}')
    comments = models.JSONField(default='{}')
    thumbnail = models.URLField(max_length=500)
    object_url = models.URLField(max_length=500)



class Result(models.Model):
    comparelist = models.ForeignKey(CompareList, on_delete=models.CASCADE)
    # selected_object_name = models.CharField(max_length=100, default="not_defined")
    # selected_object_url = models.URLField(max_length=500, default="not_defined")
    result_json = models.JSONField(default='{}')

    # selected_object_aspect

    # {
    #     "res1": {
    #         "selected_object_name": "",
    #         "selected_obj_thumbnail": "",
    #         "selected_object_url": "",
    #         "selected_object_aspect": "",
    #         "select_reason": ""
    #     },
    #
    #     "res2": {
    #         "selected_object_name": "",
    #         "selected_obj_thumbnail": "",
    #         "selected_object_url": "",
    #         "selected_object_aspect": "",
    #         "select_reason": ""
    #     }
    # }