import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key = os.getenv("API_KEY"),
    base_url = "https://api.gapgpt.app/v1"
)

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
TOOL_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a text file and return its content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "path of the file to read"},
                },
                "required": ["path"],
            },
        },
    },
]

messages = [
    {"role": "user", "content": "what is inside note.txt? summarize it in one line."}
]

while True:
    response = client.chat.completions.create(
        model="gapgpt-qwen-3.6",
        messages= messages,
        tools=TOOL_SCHEMA
    )
    message = response.choices[0].message
    messages.append(message)
    
    if not message.tool_calls:
        print(message.content)
        break

    for tool in message.tool_calls:
        args = json.loads(tool.function.arguments)
        print(f"model wants to run: read_file({args})")
        
        result = read_file(**args)
        messages.append({
            "role": "tool",
            "tool_call_id": tool.id,
            "content": result
        })