from typing import List
from textbase.models import OpenAI
from textbase import bot, Message

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")


# Load your OpenAI API key
OpenAI.api_key = api_key

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with a Financial Advisor. Feel free to ask questions or seek advice about your finances, investments, or budgeting.
The AI will provide you with information and recommendations to help you make informed financial decisions.
"""


@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Extract the last message from the history
    last_message = message_history[-1]

    # Extract user input from the last message
    user_input = last_message.get("data", {}).get("content", "")

    # Logic for the financial advisor chatbot
    if "budget" in user_input.lower():
        bot_response = "Creating and managing a budget is essential for financial stability. I can help you get started with budgeting."
    elif "investment" in user_input.lower():
        bot_response = "Investing can grow your wealth over time. Let's discuss your investment goals and risk tolerance."
    elif "retirement" in user_input.lower():
        bot_response = "Planning for retirement is crucial. We can calculate how much you need to save for a comfortable retirement."
    elif "expense tracking" in user_input.lower():
        # Add functionality for expense tracking
        bot_response = "Expense tracking is a great way to understand your spending habits. You can use apps like Mint or YNAB to track your expenses."
    elif "loan management" in user_input.lower():
        # Add functionality for loan and debt management
        bot_response = "Managing loans and debts is important. Consider paying off high-interest debts first and creating a debt repayment plan."
    elif "goal setting" in user_input.lower():
        # Add functionality for goal setting
        bot_response = "Setting financial goals is a key step. Let's define your goals and create a plan to achieve them."
    else:
        # If no specific financial topic is mentioned, use OpenAI to generate a general response.
        bot_response = OpenAI.generate(
            model="gpt-3.5-turbo",
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history
        )

    # Structure the bot's response
    response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": bot_response
                }
            ],
            "state": state
        },
        "errors": [
            {
                "message": ""
            }
        ]
    }

    return {
        "status_code": 200,
        "response": response
    }
