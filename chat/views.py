import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

HUGGING_FACE_API_KEY = "Put API Token from HuggingFace"

@csrf_exempt
def chat_response(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)  # Load JSON data
            user_input = body.get("message", "").strip()  # Get user input
        except json.JSONDecodeError:
            return JsonResponse({"response": "Invalid data received."})

        # Check that user input is not empty
        if not user_input:
            return JsonResponse({"response": "Please enter a message."})

        # Set request headers and parameters
        headers = {
            "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
        }
##################################################################
        payload = {
            "inputs": user_input,
            "parameters": {
                "temperature": 0.2,  # Set temperature to control response randomness
                "max_length": 100,   # Maximum token count
                "top_k": 40,         # Limit search to top options
                "top_p": 0.9         # Control probability distribution for words
            }
        }
################################################################
        # # Using GPT-3.5 model
        # response = requests.post("https://api-inference.huggingface.co/models/gpt-3.5-turbo",
        #                          headers=headers, json=payload)

        # Using gpt-neo model
        response = requests.post("https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B",
                                 headers=headers, json=payload)

        # # Using gpt-j model
        # response = requests.post("https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B",
        #                          headers=headers, json=payload)
        #
        # # Using gpt-2 model
        # response = requests.post("https://api-inference.huggingface.co/models/gpt2",
        #                          headers=headers, json=payload)

################################################################

        # Check API response and process it
        if response.status_code == 200:
            model_output = response.json()[0].get("generated_text", "No response received from model.")
            model_output = remove_repeated_phrases(model_output)  # Remove repeated phrases
        else:
            model_output = f"Error: {response.status_code} - {response.text}"

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