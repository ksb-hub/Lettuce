# aspectapp/views.py

import openai
from decouple import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AspectProductsView(APIView):
    def get(self, request):
        products = request.query_params.getlist("product")

        if len(products) < 2:
            return Response({"에러": "적어도 두 가지 제품을 기입하세요."}, status=status.HTTP_400_BAD_REQUEST)

        aspect_list = self.generate_comparison_questions(products[0], products[1])
        return Response({"비교 결과": aspect_list})

    def generate_comparison_questions(self, product1, product2):
        openai.api_key = config('OPENAI_API_KEY')

        prompt = f"{product1}과 {product2}의 비교기준을 6가지로 나타내세요."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        aspect_list = response.choices[0].text.strip()
        aspect_names = aspect_list.split(', ')

        numbered_aspects = [f"{idx + 1}. {aspect}" for idx, aspect in enumerate(aspect_names)]

        return numbered_aspects