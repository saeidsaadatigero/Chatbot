import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

HUGGING_FACE_API_KEY = "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"  # توکن هاگینگ فیس خود را اینجا قرار دهید

@csrf_exempt
def chat_response(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)  # بارگذاری داده‌های JSON
            user_input = body.get("message", "").strip()  # دریافت ورودی کاربر
        except json.JSONDecodeError:
            return JsonResponse({"response": "داده‌های دریافتی نامعتبر است."})

        # بررسی اینکه ورودی کاربر خالی نباشد
        if not user_input:
            return JsonResponse({"response": "لطفاً پیامی وارد کنید."})


        # تنظیم هدرها و پارامترهای درخواست
        headers = {
            "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
        }
##################################################################
        payload = {
            "inputs": user_input,
            "parameters": {
                "temperature": 0.2,  # تنظیم دما برای کنترل تصادفی بودن پاسخ
                "max_length": 100,   # حداکثر تعداد توکن‌ها
                "top_k": 40,         # محدود کردن جستجوی کلمات به بهترین گزینه‌ها
                "top_p": 0.9        # کنترل روی احتمال توزیع کلمات
            }
        }
################################################################
        # # استفاده از مدل GPT-3.5
        # response = requests.post("https://api-inference.huggingface.co/models/gpt-3.5-turbo",
        #                          headers=headers, json=payload)


        # استفاده از مدل gpt-neo
        response = requests.post("https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B",
                                 headers=headers, json=payload)

        # # استفاده از مدل gpt-j
        # response = requests.post("https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B", headers=headers,
        #                          json=payload)
        #
        # # استفاده از مدل gpt-2
        # response = requests.post("https://api-inference.huggingface.co/models/gpt2", headers=headers, json=payload)

################################################################


#         # بررسی پاسخ API و پردازش آن
#         if response.status_code == 200:
#             model_output = response.json()[0].get("generated_text", "پاسخی از مدل دریافت نشد.")
#         else:
#             model_output = f"خطا: {response.status_code} - {response.text}"
#             model_output = remove_repeated_phrases(model_output)  # حذف عبارات تکراری
#
#
#         return JsonResponse({"response": model_output})
#
#     return JsonResponse({"error": "Invalid request"}, status=400)
#
# def index(request):
#     return render(request, 'chat/index.html')

        # بررسی پاسخ API و پردازش آن
        if response.status_code == 200:
            model_output = response.json()[0].get("generated_text", "پاسخی از مدل دریافت نشد.")
            model_output = remove_repeated_phrases(model_output)  # حذف عبارات تکراری
        else:
            model_output = f"خطا: {response.status_code} - {response.text}"

        return JsonResponse({"response": model_output})

    return JsonResponse({"error": "Invalid request"}, status=400)


def remove_repeated_phrases(text):
    words = text.split()
    seen = set()
    result = []

    for word in words:
        if word not in seen:
            seen.add(word)
            result.append(word)

    return ' '.join(result)


def index(request):
    return render(request, 'chat/index.html')
