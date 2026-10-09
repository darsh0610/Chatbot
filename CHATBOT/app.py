"""
Flask Web Server for AI Course Advisor Chatbot
-----------------------------------------------
Serves the chat UI and exposes a /chat API endpoint.
Run with: python app.py
"""

import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # for session management

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("No API key found! Add GROQ_API_KEY to your .env file.")

llm = ChatGroq(
    groq_api_key=api_key,
    model="openai/gpt-oss-120b",
    temperature=0.7
)

SYSTEM_PROMPT = (
    "You are a friendly academic advisor chatbot for engineering students. "
    "You help answer questions about courses, study tips, career guidance, "
    "and academic planning in a clear, encouraging, and concise way. "
    "Use bullet points and structure when helpful."
)

# In-memory store: session_id -> chat_history
chat_sessions = {}


def get_history(session_id):
    if session_id not in chat_sessions:
        chat_sessions[session_id] = [SystemMessage(content=SYSTEM_PROMPT)]
    return chat_sessions[session_id]


@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = os.urandom(16).hex()
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    session_id = session.get("session_id", "default")
    history = get_history(session_id)

    history.append(HumanMessage(content=user_message))

    try:
        response = llm.invoke(history)
        reply = response.content
        history.append(AIMessage(content=reply))
        return jsonify({"reply": reply})
    except Exception as e:
        history.pop()  # remove the failed human message
        return jsonify({"error": str(e)}), 500


@app.route("/reset", methods=["POST"])
def reset():
    session_id = session.get("session_id", "default")
    chat_sessions[session_id] = [SystemMessage(content=SYSTEM_PROMPT)]
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("\n[OK] AI Course Advisor is running!")
    print("   Open your browser at: http://localhost:5000\n")
    app.run(debug=True, port=5000)
