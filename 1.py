import os
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIResponsesModel(
    "gapgpt-qwen-3.6",
    provider=OpenAIProvider(
        base_url="https://api.gapgpt.app/v1",
        api_key="<your token>",
    ),
)

NOTE_FILE = "note.txt"

def calculation(expression: str) -> str:
    """This is a simple function for evaluation an expression"""
    
    if not set(expression) <= set("1234567890-+*/() "):
        return "Error: you enterd wrong expression character."

    try:
        return str(eval(expression))
    except Exception as error:
        return "Error: {error}"
        
def addnote(note: str) -> str:
    """This is for adding note to a file """
    with open(NOTE_FILE, "a", encoding="utf-8") as file:
        file.write(f"- {note}\n")
    return "note has been saved."


def readnote() -> str:
    """This function read the note file"""
    if not os.path.exists(NOTE_FILE):
        return "Thre is no note file exists."
    with open(NOTE_FILE, "r", encoding="utf-8") as file:
        return file.read()


agent = Agent(
    model,
    tools=[calculation, readnote, addnote],
    instructions=(
        "You are a helpful personal assistant running 100% locally. "
        "Use your tools whenever they can help answer the question. "
        "Keep your answers short and friendly."
    ),
)


def main():
    print("Local agent ready! Type 'quit' to exit.\n")
    history = []
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("quit", "exit"):
            break
        result = agent.run_sync(user_input, message_history=history)
        history = result.all_messages()
        print(f"\nAgent: {result.output}\n")


if __name__ == "__main__":
    main()