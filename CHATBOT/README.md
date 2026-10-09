# AI Chatbot with LangChain — Course Advisor Bot

A beginner-friendly conversational chatbot built with LangChain that remembers
the conversation and answers like a friendly academic advisor.

## How it works (plain-English breakdown)

1. **LLM (the brain)** — `ChatGroq` connects to a free, fast Llama model
   hosted by Groq. This is the thing that actually generates replies.
2. **System message** — a one-time instruction that tells the bot *who it is*
   (a friendly course advisor), set before the conversation starts.
3. **Chat history / memory** — every message (yours and the bot's) is stored
   in a list called `chat_history`. Each turn, the *entire* history is sent
   back to the LLM — that's how it "remembers" earlier things you said.
4. **The loop** — a simple `while True` loop keeps asking for your input,
   sends it to the bot, prints the reply, and repeats until you type `quit`.

## Setup

1. Create a free Groq account: https://console.groq.com
2. Get an API key from the dashboard.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and paste your key:
   ```
   cp .env.example .env
   ```
   Then edit `.env` so it looks like:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here
   ```

## Run it

```
python chatbot.py
```

Then just start chatting. Type `quit` to exit.

## Ideas to extend it (good for making the project "yours" in a report)

- Add a **file-based memory** so chat history survives after closing the program
- Swap the system prompt to make it a *different* kind of bot (coding tutor, resume reviewer, etc.)
- Add a **Streamlit UI** (`pip install streamlit`) for a simple web chat interface
- Add **RAG**: load your own notes/PDFs so the bot can answer questions about your specific course material

## Why this counts as "using LangChain agents"

This version uses LangChain's core LLM + memory pattern. Once comfortable,
the natural next step is `LangGraph` or LangChain's `AgentExecutor`, where
the bot can also take actions (like looking things up) instead of just
replying with text — useful for your next project.
