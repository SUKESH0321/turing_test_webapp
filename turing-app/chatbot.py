import requests

API_URL = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}

def chat_with_gpt(prompt):
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        result = response.json()
        print("DEBUG Response:", result)
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Request failed: {e}"

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            break
        response = chat_with_gpt(user_input)
        print("chatbot:", response)
