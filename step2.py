from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

clinet = OpenAI(
    api_key = os.getenv("API_KEY"),
    base_url = "https://api.gapgpt.app/v1"
)

messages = []

while True:
    
    user_input = input("You: ")
    if user_input.strip().lower() in ("exit", "quit"):
        break
    
    messages.append({"role": "user", "content": user_input})
    response = clinet.chat.completions.create(
        model="gapgpt-qwen-3.6",
        messages= messages
    )
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    print("Bot:", reply)