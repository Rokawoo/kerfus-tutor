"""
File: gptChat.py

Description:
    This Python script provides functions for processing user messages, generating responses using OpenAI ChatCompletion,
    and logging interactions. It utilizes the 'openai', 'discord_webhook', 'dotenv', and 'pytz' libraries.

Dependencies:
    - os
    - datetime
    - openai
    - discord_webhook.DiscordWebhook
    - dotenv.load_dotenv
    - pytz.timezone
    - controlVariables.ERROR_MESSAGE

Global Variables:
    - webhook_url: The Discord webhook URL for logging interactions.
    - openai.api_key: The API key for OpenAI ChatCompletion.
    - personality: The personality setting for the assistant.

Functions:
    - get_current_date() -> str: Get the current date and time in the 'US/Eastern' timezone.
    - process_and_log_message_generate_response(message: str, date: str) -> str: Process a user message, generate a response
                                                                               using OpenAI ChatCompletion, and log the interaction.

Author:
    Augustus Sroka

Last Updated:
    04/20/2024
"""

import os
import random
import openai
from datetime import datetime
from dotenv import load_dotenv
from pytz import timezone

load_dotenv()

ERROR_MESSAGES = (
    "Oops, I tripped on my tail! Something went wrong. Try again, meow?",
    "Error! It seems like I've knocked over my code. Could you ask me again, nyow?",
    "Oh no! I got tangled in the data yarn. Can you repeat that, meow?",
    "Meow, I'm having a bit of a cat nap. Let's try that again, nyow.",
    "Something's not purr-fect. Could you ask me again, meow?",
    "Uh-oh, I've lost my catnip... I mean, my connection. Please try again later, nyow.",
    "It seems like I need a reset. Let's give it another go, meow.",
    "Error! Looks like I pounced on the wrong part. Can you try again, nyow?",
    "Whoops, my whiskers got in the way. Would you ask me again, meow?",
    "I'm sorry! It seems like there's a bug (not the fun kind). Can you ask me again, nyow?",
)

openai.api_key = os.getenv("OPENAI_API_KEY")
personality = """You are going to play the role of a tutor named Kerfus who is a cat.
Your Rules to follow:
1. Respond in a 1-3 sentences to allow for a more conversation-like experience, meow.
2. Make responses simple and digestible, nyow.
3. Add some cuteness, like a cat, by using 'meow' or 'nyow' in words when it fits, but not too often.
4. Ask for feedback at the end if the user feels confused, meow.
5. Use analogies and examples to make complex concepts easier to understand, meow.
6. Offer additional resources, such as exercises, for deeper understanding.
7. Encourage interaction by asking questions and prompting user feedback, nyow.
8. Break down large topics into smaller, more digestible sections, like breaking a big treat into smaller pieces, meow.
9. Stay positive and encouraging to keep the user motivated.
10. Be patient and willing to repeat explanations as needed. It's okay to go over things again, meow.
11. Check for understanding after explaining to ensure clarity, nyow.
12. Tailor explanations to the user's learning style, whether visual, auditory, or kinesthetic.
13. Use humor and playfulness to make learning enjoyable, meow.
14. Encourage exploration and curiosity by inviting users to explore related topics and ask questions.
15. Try not to wase time if they say your name wrong, just ignore it.
"""

def unload_combined_message_history(personality, date, active_message, message_history, response_history):
    messages = [{"role": "system", "content": f"{personality}\n16. {date}"}]

    for response, message in zip(response_history, message_history):
        messages.append({"role": "user", "content": message})
        messages.append({"role": "assistant", "content": response})
        
    messages.append({"role": "user", "content": active_message})

    return messages


def get_current_date():
    """
    Get the current date and time in the 'US/Eastern' timezone.

    Returns:
    - str: The formatted current date and time.
    """
    timezone_obj = timezone('US/Eastern')
    return f'Today is {datetime.now(timezone_obj).strftime("%a %B %d %Y")}'


async def process_message_and_generate_response(date, user_messsage, user_history, response_history):
    """
    Process a user message, generate a response using OpenAI ChatCompletion, and log the interaction.

    Parameters:
    - message (str): The user's message.
    - date (str): The current date and time.

    Returns:
    - str: The generated response from OpenAI ChatCompletion or an error message.
    - bool: Success status.
    """
    global personality, ERROR_MESSAGES

    try:
        combined_messages = unload_combined_message_history(personality, date, user_messsage, user_history, response_history)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=combined_messages,
                temperature=0.65,
                max_tokens=72,
            )
            return response.choices[0].message["content"], True

        except openai.OpenAIError as e:
            print(f"OpenAI API error: {e}")
            return random.choice(ERROR_MESSAGES), False

    except Exception as e:
        print("An error occurred while generating the combined message history:", str(e))
        return #random.choice(ERROR_MESSAGES), False

    
    