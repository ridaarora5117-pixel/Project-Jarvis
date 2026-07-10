
import ollama 
import datetime
import requests

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
        "If the user asks about weather without specifying a city, always call get_weather with no arguments."
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

def get_weather(city=None, country_code=None):
    if city is None:
        city_data = requests.get("http://ip-api.com/json/").json()
        city = city_data.get("city")
        country = city_data.get("countryCode")
    else:
        country = country_code

    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=5"
    region_data = requests.get(url).json()
    if not region_data.get("results"):
        return f"Sorry, I couldn't find weather data for {city}."
    
    results = region_data["results"]
    
    if country:
        match = next((r for r in results if r.get("country_code") == country), results[0])
    else:
        match = results[0]

    latitude = match["latitude"]
    longitude = match["longitude"]
    weather = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true").json()
    temperature = weather["current_weather"]["temperature"]
    return f"The current temperature in {city} is {temperature}°C."

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
    },
    {
        "type": "function",
        "function" : {
            "name": "get_weather",
            "description": "Get the current weather for a specified city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to get weather for."
                },
                "country_code": {
                    "type": "string",
                    "description": "Two letter country code e.g. CA, US, GB. Use when user specifies a country."
                }
            },
            "required": []
}
        }
    }
]




print ("Jarvis is online. Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if "thank you" in user_input.lower() or "thanks" in user_input.lower():
        print("Jarvis: You're welcome!")
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
        elif tool_name == "get_weather":
            city = tool_args.get("city", None)
            country_code = tool_args.get("country_code", None)
            result = get_weather(city, country_code)
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

