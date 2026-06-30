
import ollama 

messages = []
print ("Jarvis is online. Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    messages.append({"role": "user", "content": user_input})
    response = ollama.chat(model="llama3.1", messages=messages)
    reply = response["message"]["content"]
    print(f"Jarvis: {reply}")
    messages.append({"role": "assistant", "content": reply})

