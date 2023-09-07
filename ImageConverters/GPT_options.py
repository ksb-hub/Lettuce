import openai
from decouple import config
# def summarize(prod_dict):
#     openai.api_key = config('OPENAI_API_KEY')
#     completion = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#         {
#             "role": "system",
#             "content": "당신은 내용을 보고 상품명, 내용, 상품 정보로 요약합니다."
#         },
#         {
#             'role': 'user',
#             'content': f'{prod_dict}'
#         },
#         ],
#     )
#
#     return completion.choices[0].message.content
#
# def get_result(prod_dict):
#     openai.api_key = config('OPENAI_API_KEY')
#     sum_text_list = []
#     for index, obj in enumerate(prod_dict['products']):
#         sum_text_list.append(summarize(obj))
#
#     # print(sum_text_list)
#
#
#     try:
#         aspect = ["성능", "만족도", "브랜드"]
#         completion = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#             {
#                 "role": "system",
#                 "content": f"당신은 상품별로 상품명, 상품 정보, 내용을 보고 {aspect}에 담긴 측면별 추천 상품을 반환합니다." + "selected_object_num는 상품 번호로 넣어줘 예) 1번 상품이 선택돼면 selected_object_num에는 1을 넣어줘." + "그리고 측면 갯수 만큼 비교해줘야 해." + '\n 답변 양식: [{"selected_object_aspect": "", "selected_object_num": "", "select_reason": ""}]'
#             },
#             {
#                 "role": "user",
#                 "content": f"{sum_text_list}"
#             }
#             ],
#         )
#
#         recommendation = completion.choices[0].message.content
#
#         return recommendation
#     except Exception as e:
#         return(e)
def get_result(prod_dict, aspects):
    openai.api_key = config('OPENAI_API_KEY')
    try:
        aspect = aspects
        aspect_length = len(aspect)
        # print(prod_dict)
        obj_length = len(prod_dict["products"])
        # print(obj_length)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
            {
                "role": "system",
                # "content": f"당신은 상품별로 상품명, 상품 정보, 내용을 보고 {aspect}에 담긴 측면별 추천 상품을 반환합니다. 즉, 측면 수 만큼 비교해줘야 해." + "selected_object_num는 상품 번호로 넣어줘 예) 1번 상품이 선택돼면 selected_object_num에는 1을 넣어줘." + '\n 답변 양식: [{"selected_object_aspect": "", "selected_object_num": "", "select_reason": ""}]'
                # "content": f'당신은 상품별로 object_name, img_text, obj_info, comments를 보고 \n측면 : {aspect}\n 에 담긴 각 측면별 추천 상품을 반환합니다. 전체 정보를 고려한 종합적인 결론을 내야합니다. 반드시, {aspect_length}개의 결론을 5줄 이상으로 아주 상세하게 반환해야 합니다.' + "또한 selected_object_num는 상품 번호로 넣어줘 예) 1번 상품이 선택 되면 selected_object_num 의 값은 1" + '\n 답변 예시: [{"selected_object_aspect": "비교 기준", "selected_object_num":'+ f'"1~{obj_length}'+ ' 사이의 상품 번호", "select_reason": "선택 이유" }]'
                "content": f'당신은 상품별 제공된 모든 정보를 보고 \n측면 : {aspect}\n 에 담긴 각 측면별 가장 뛰어난 상품을 반환합니다. 전체 정보를 고려한 다른 상품들과의 차이점을 위주로 결론을 내야합니다. 반드시, {aspect_length}개의 결론을 5줄 이상으로 아주 상세하게 반환해야 합니다.' + "또한 selected_object_num는 상품 번호로 넣어줘 예) 1번 상품이 선택 되면 selected_object_num 의 값은 1" + '\n 답변 예시: [{"selected_object_aspect": "비교 기준", "selected_object_num":' + f'"1~{obj_length}' + ' 사이의 상품 번호", "select_reason": "선택 이유" }]'
            },
            {
                "role": "user",
                "content": f"{prod_dict}"
            }
            ],
        )
        recommendation = completion.choices[0].message.content
        return recommendation
    except Exception as e:
        return(e)