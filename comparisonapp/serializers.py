from rest_framework import serializers

class CompareProductsSerializer(serializers.Serializer):
    product1 = serializers.CharField()
    product2 = serializers.CharField()
    recommendation = serializers.CharField()