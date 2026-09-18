from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key = os.getenv("API_KEY"),
    base_url = "https://api.gapgpt.app/v1"
)

response = client.chat.completions.create(
    model="gapgpt-qwen-3.6",
    messages= [
        {
            "role": "user", "content": "explain what is an ai agent is in one sentence."
        }
    ]
)
print(response.choices[0].message.content)