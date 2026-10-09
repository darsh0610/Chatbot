"""
Flask Web Server for AI Course Advisor Chatbot
-----------------------------------------------
Serves the chat UI and exposes a /chat API endpoint.
Optimized for local running and Vercel Serverless deployment.
"""

import os
from flask import Flask, render_template, request, jsonify, session, send_from_directory
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

app.secret_key = os.getenv("SECRET_KEY", "academic-advisor-secret-key-2024")

SYSTEM_PROMPT = (
    "You are a friendly academic advisor chatbot for engineering students. "
    "You help answer questions about courses, study tips, career guidance, "
    "and academic planning in a clear, encouraging, and concise way. "
    "Use bullet points and structure when helpful."
)


def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return ChatGroq(
        groq_api_key=api_key,
        model="openai/gpt-oss-120b",
        temperature=0.7
    )


@app.route("/chat", methods=["POST"])
@app.route("/api/index/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    llm = get_llm()
    if not llm:
        return jsonify({
            "error": "GROQ_API_KEY is not configured in Vercel environment variables. Please add GROQ_API_KEY in Vercel Project Settings."
        }), 500

    history_data = session.get("history", [])

    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    for item in history_data:
        if item.get("role") == "user":
            messages.append(HumanMessage(content=item.get("content", "")))
        elif item.get("role") == "assistant":
            messages.append(AIMessage(content=item.get("content", "")))

    messages.append(HumanMessage(content=user_message))

    try:
        response = llm.invoke(messages)
        reply = response.content

        history_data.append({"role": "user", "content": user_message})
        history_data.append({"role": "assistant", "content": reply})

        if len(history_data) > 20:
            history_data = history_data[-20:]

        session["history"] = history_data
        session.modified = True

        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/reset", methods=["POST"])
@app.route("/api/index/reset", methods=["POST"])
def reset():
    session.pop("history", None)
    return jsonify({"status": "ok"})


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=["GET", "POST"])
def catch_all(path):
    if path.startswith("static/"):
        filename = path[len("static/"):]
        return send_from_directory(app.static_folder, filename)

    if request.method == "POST":
        data = request.get_json(silent=True)
        if (data and "message" in data) or path.endswith("chat") or request.path.endswith("chat"):
            return chat()
        if path.endswith("reset") or request.path.endswith("reset"):
            return reset()

    return render_template("index.html")


if __name__ == "__main__":
    print("\n[OK] AI Course Advisor is running!")
    print("   Open your browser at: http://localhost:5000\n")
    app.run(debug=True, port=5000)
