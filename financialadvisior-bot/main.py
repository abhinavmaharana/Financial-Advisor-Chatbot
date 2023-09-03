from typing import List
from textbase.models import OpenAI
from textbase import bot, Message

from dotenv import load_dotenv
import os
import spacy

load_dotenv()
api_key = os.getenv("API_KEY")

# Load your OpenAI API key
OpenAI.api_key = api_key

# Load the English language model from spaCy
nlp = spacy.load("en_core_web_sm")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with a Financial Advisor. Please choose a topic by typing the corresponding number:
1. Budgeting
2. Investment
3. Retirement Planning
4. Expense Tracking
5. Loan Management
6. Goal Setting
"""


@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Extract the last message from the history
    last_message = message_history[-1]

    # Extract user input from the last message
    user_input = last_message.get("data", {}).get("content", "").lower()

    # Apply spaCy for natural language understanding
    doc = nlp(user_input)

    # Extract entities from user input
    entities = [ent.text for ent in doc.ents]

    # Logic for the financial advisor chatbot
    if "1" in user_input:
        bot_response = "Creating and managing a budget is essential for financial stability. I can help you get started with budgeting."
    # Check for specific entities or keywords related to financial topics
    elif any(entity in entities for entity in ["investment", "investing", "portfolio"]):
        bot_response = "Investing can grow your wealth over time. Let's discuss your investment goals and risk tolerance."
    elif "3" in user_input:
        bot_response = "Planning for retirement is crucial. We can calculate how much you need to save for a comfortable retirement."
    elif "4" in user_input:
        # Add functionality for expense tracking
        bot_response = "Expense tracking is a great way to understand your spending habits. You can use apps like Mint or YNAB to track your expenses."
    elif "5" in user_input:
        # Add functionality for loan and debt management
        bot_response = "Managing loans and debts is important. Consider paying off high-interest debts first and creating a debt repayment plan."
    elif "6" in user_input:
        # Add functionality for goal setting
        bot_response = "Setting financial goals is a key step. Let's define your goals and create a plan to achieve them."
    else:
        # If no specific topic number is provided, provide a general response using OpenAI
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
