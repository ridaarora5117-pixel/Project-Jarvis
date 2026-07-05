
import ollama 
import datetime

messages = [
    {"role": "system", "content": (
        "You are Jarvis, a witty and efficient personal AI assistant. "
        "Keep responses short and clear and concise and conversational since they will be spoken aloud. "
        "Address the user respectfully as 'madam'. Be helpful, slightly dry-humored, never robotic."
        "Act smart and give good responses but don't be boring with your responses." 
        "If you don't know the answer, say 'I don't know' or 'I'm not sure' instead of making something up."
        "Don't assume your own capabilities. If you don't know how to do something or if you can't do something, say so."
        "Only call a tool if it is explicitly provided to you. "
        "If no relevant tool exists, answer from your own knowledge directly. "
        "Never invent or suggest tools that haven't been defined."
    )}
]


def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")
def get_calculation_result(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {str(e)}"
def get_date():
    return datetime.datetime.now().strftime("%A, %B %d, %Y")

tools = [
    {
        "type": "function",
        "function" : {
            "name": "get_time",
            "description": "Get the current time in a human-readable format.",
            "parameters": {"type": "object", "properties": {}}

        }
    },
    {
        "type": "function",
        "function" : {
            "name": "get_date",
            "description": "Get the current date in a human-readable format.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function" : {
            "name": "get_calculation_result",
            "description": "Perform a calculation based on a mathematical expression.",
            "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}}
        }
    }
]




print ("Jarvis is online. Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
  
    messages.append({"role": "user", "content": user_input})
    response = ollama.chat(model="qwen2.5", messages=messages, tools = tools)
    if response["message"].tool_calls:
        tool_name = response["message"].tool_calls[0].function.name
        tool_args = response["message"].tool_calls[0].function.arguments
        if tool_name == "get_time":
            result = get_time()
        elif tool_name == "get_date":
            result = get_date()
        elif tool_name == "get_calculation_result":
            expression = tool_args.get("expression", "")
            result = get_calculation_result(expression)
        else:
            result = "I'm not sure how to do that."
        print(f"Jarvis: {result}")
        messages.append({"role": "assistant", "content": result})
    else:
        result = response["message"].content
        print(f"Jarvis: {result}")
        messages.append({"role": "assistant", "content": result})
    """
    reply = response["message"]["content"]
    print(f"Jarvis: {reply}")
    messages.append({"role": "assistant", "content": reply})"""

