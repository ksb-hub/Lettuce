import openai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decouple import config

class CompareProductsView(APIView):
    def get(self, request):
        selected_aspect = request.query_params.get("selected_aspect")
        product1 = request.query_params.get("product1")
        product2 = request.query_params.get("product2")

        if not selected_aspect or not product1 or not product2:
            return Response({"에러": "적절한 요청 데이터를 제공하세요."}, status=status.HTTP_400_BAD_REQUEST)

        recommendation = self.generate_recommendation(product1, product2, selected_aspect)
        return Response({"추천 결과": recommendation})

    def generate_recommendation(self, product1, product2, selected_aspect):
        openai.api_key = config('OPENAI_API_KEY')

        prompt = f"{selected_aspect} 측면에서 {product1}과 {product2}을 비교한 후 더 좋은 제품을 추천해주세요."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        recommendation = response.choices[0].text.strip()

        return recommendation