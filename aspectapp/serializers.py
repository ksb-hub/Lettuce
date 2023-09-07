# aspectapp/serializers.py

from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    productName = serializers.CharField(max_length=100)
    productReview = serializers.CharField()
    mallProductUrl = serializers.URLField()