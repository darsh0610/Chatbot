"""
AI Chatbot with LangChain - Beginner Project
----------------------------------------------
A simple conversational chatbot that remembers chat history.
Uses Groq's free-tier API (fast + free Llama models) via LangChain.

Why Groq instead of OpenAI?
- Free tier available (no credit card needed for basic use)
- Very fast responses
- Works the same way LangChain talks to any LLM provider

SETUP STEPS (do this before running):
1. Create a free account at https://console.groq.com
2. Get an API key from the dashboard
3. Install required packages:
       pip install langchain langchain-groq python-dotenv
4. Create a file named ".env" in this same folder with this line:
       GROQ_API_KEY=your_key_here
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# ---- Step 1: Load the API key from .env file ----
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "No API key found! Create a .env file with GROQ_API_KEY=your_key_here"
    )

# ---- Step 2: Set up the LLM (the "brain" of the chatbot) ----
llm = ChatGroq(
    groq_api_key=api_key,
    model="openai/gpt-oss-120b",     # largest model available on this account
    temperature=0.7                  # 0 = very predictable, 1 = more creative
)

# ---- Step 3: Set up a system message (defines the bot's personality/role) ----
system_prompt = SystemMessage(
    content=(
        "You are a friendly academic advisor chatbot for engineering students. "
        "You help answer questions about courses, study tips, and career guidance "
        "in a clear, encouraging, and concise way."
    )
)

# ---- Step 4: Keep track of conversation history (this gives the bot "memory") ----
chat_history = [system_prompt]


def chat():
    print("=" * 50)
    print(" AI Course Advisor Chatbot (LangChain + Groq)")
    print(" Type 'quit' to exit")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["quit", "exit"]:
            print("Bot: Goodbye! Good luck with your studies!")
            break

        # Add the user's message to history
        chat_history.append(HumanMessage(content=user_input))

        # Send the whole conversation so far to the LLM
        response = llm.invoke(chat_history)

        # Add the bot's reply to history too (so it remembers it next turn)
        chat_history.append(AIMessage(content=response.content))

        print(f"Bot: {response.content}")


if __name__ == "__main__":
    chat()
