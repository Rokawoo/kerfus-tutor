from collections import deque

def unload_combined_message_history(personality, date, active_message, message_history, response_history):
    messages = [{"role": "system", "content": date + "\n" + personality+ "\n"}]

    for response, message in zip(response_history, message_history):
        messages.append({"role": "user", "content": message+ "\n"})
        messages.append({"role": "assistant", "content": response+ "\n"})
        
    messages.append({"role": "user", "content": active_message+ "\n"})

    return messages

message_history = deque([
    "Hello, I need help with my code.",
    "I'm trying to fix a bug.",
    "Could you suggest a good Python library for data processing?"
], maxlen=10)

response_history = deque([
    "Sure, I'm here to help. What's the problem?",
    "Okay, can you describe the bug?",
    "I suggest using pandas for data processing. It's quite popular."
], maxlen=10)

personality = "I am a helpful assistant."

chat_messages = unload_combined_message_history(personality, "DATE", "ACTIVE", message_history, response_history)

print(chat_messages)
