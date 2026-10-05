from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import ollama

from rag import search_knowledge

app = FastAPI()


class Question(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
def home():

    return """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>ShopEase AI Customer Support</title>

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f3f4f6;
            color: #111827;
            transition: 0.3s;
        }

        body.dark {
            background: #111827;
            color: #f9fafb;
        }

        .app {
            max-width: 1000px;
            margin: 30px auto;
            padding: 20px;
        }

        .header {
            background: white;
            padding: 22px;
            border-radius: 16px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        body.dark .header,
        body.dark .card,
        body.dark .chat-box {
            background: #1f2937;
            color: white;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo {
            font-size: 40px;
        }

        h1 {
            margin: 0;
            font-size: 26px;
        }

        .subtitle {
            color: #6b7280;
            margin-top: 5px;
        }

        body.dark .subtitle {
            color: #d1d5db;
        }

        .top-buttons {
            display: flex;
            gap: 8px;
        }

        .small-btn {
            border: none;
            padding: 10px 13px;
            border-radius: 8px;
            cursor: pointer;
            background: #e5e7eb;
            font-size: 15px;
        }

        .small-btn:hover {
            transform: scale(1.03);
        }

        .main {
            margin-top: 20px;
        }

        .card {
            background: white;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }

        .suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 12px;
        }

        .suggestion {
            border: 1px solid #d1d5db;
            background: #f9fafb;
            padding: 10px 14px;
            border-radius: 20px;
            cursor: pointer;
        }

        .suggestion:hover {
            background: #e5e7eb;
        }

        body.dark .suggestion {
            background: #374151;
            color: white;
            border-color: #4b5563;
        }

        textarea {
            width: 100%;
            height: 100px;
            margin-top: 15px;
            padding: 14px;
            border: 1px solid #d1d5db;
            border-radius: 10px;
            resize: none;
            font-size: 16px;
            background: white;
            color: #111827;
        }

        body.dark textarea {
            background: #374151;
            color: white;
            border-color: #4b5563;
        }

        .ask-btn {
            width: 100%;
            margin-top: 12px;
            padding: 14px;
            border: none;
            border-radius: 10px;
            background: #2563eb;
            color: white;
            font-size: 17px;
            cursor: pointer;
        }

        .ask-btn:hover {
            background: #1d4ed8;
        }

        .chat-box {
            background: white;
            padding: 20px;
            border-radius: 16px;
            min-height: 100px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }

        .message {
            padding: 14px;
            margin-bottom: 12px;
            border-radius: 12px;
            line-height: 1.5;
        }

        .user-message {
            background: #dbeafe;
            color: #1e3a8a;
        }

        .ai-message {
            background: #f3f4f6;
        }

        body.dark .ai-message {
            background: #374151;
        }

        body.dark .user-message {
            background: #1e40af;
            color: white;
        }

        .feedback {
            margin-top: 10px;
            display: flex;
            gap: 8px;
        }

        .feedback button {
            border: none;
            padding: 8px 12px;
            border-radius: 8px;
            cursor: pointer;
        }

        .escalation {
            margin-top: 12px;
            padding: 14px;
            background: #fff3cd;
            color: #856404;
            border-radius: 10px;
        }

        .support-btn {
            margin-top: 10px;
            padding: 10px 15px;
            border: none;
            border-radius: 8px;
            background: #dc2626;
            color: white;
            cursor: pointer;
        }

        .loading {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .dot {
            width: 9px;
            height: 9px;
            background: #2563eb;
            border-radius: 50%;
            animation: bounce 1s infinite;
        }

        .dot:nth-child(2) {
            animation-delay: 0.15s;
        }

        .dot:nth-child(3) {
            animation-delay: 0.3s;
        }

        @keyframes bounce {

            0%, 80%, 100% {
                transform: translateY(0);
            }

            40% {
                transform: translateY(-7px);
            }

        }

        .history-title {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .clear-btn {
            border: none;
            background: #ef4444;
            color: white;
            padding: 8px 12px;
            border-radius: 8px;
            cursor: pointer;
        }

        .empty {
            color: #6b7280;
            text-align: center;
            padding: 20px;
        }

    </style>

</head>


<body>

<div class="app">

    <div class="header">

        <div class="brand">

            <div class="logo">🛒</div>

            <div>
                <h1>ShopEase AI</h1>

                <div class="subtitle">
                    AI Customer Support
                </div>
            </div>

        </div>

        <div class="top-buttons">

            <button class="small-btn" onclick="toggleDarkMode()">
                🌙
            </button>

            <button class="small-btn" onclick="clearChat()">
                🗑️ Clear
            </button>

        </div>

    </div>


    <div class="main">

        <div class="card">

            <h2>📋 Suggested Questions</h2>

            <div class="suggestions">

                <button class="suggestion"
                    onclick="setQuestion('What is the return policy?')">
                    Return Policy
                </button>

                <button class="suggestion"
                    onclick="setQuestion('How long does a refund take?')">
                    Refund Status
                </button>

                <button class="suggestion"
                    onclick="setQuestion('How long does shipping take?')">
                    Shipping
                </button>

                <button class="suggestion"
                    onclick="setQuestion('How can I track my order?')">
                    Order Tracking
                </button>

                <button class="suggestion"
                    onclick="setQuestion('Can I cancel my order?')">
                    Order Cancellation
                </button>

                <button class="suggestion"
                    onclick="setQuestion('What payment methods do you accept?')">
                    Payment Methods
                </button>

            </div>

        </div>


        <div class="card">

            <h2>💬 Ask ShopEase AI</h2>

            <textarea
                id="question"
                placeholder="Type your question here..."
            ></textarea>

            <button class="ask-btn" onclick="askAI()">
                🤖 Ask AI
            </button>

        </div>


        <div class="chat-box">

            <div class="history-title">

                <h2>💬 Chat History</h2>

                <button class="clear-btn" onclick="clearChat()">
                    Clear Chat
                </button>

            </div>

            <div id="chatHistory">

                <div class="empty">
                    Your conversation will appear here.
                </div>

            </div>

        </div>

    </div>

</div>


<script>

    let chatHistory = [];


    function setQuestion(question) {

        document.getElementById("question").value = question;

        document.getElementById("question").focus();

    }


    function toggleDarkMode() {

        document.body.classList.toggle("dark");

    }


    function clearChat() {

        chatHistory = [];

        document.getElementById("chatHistory").innerHTML =
            "<div class='empty'>Your conversation will appear here.</div>";

    }


    function addMessage(question, answer, escalate) {

        const history = document.getElementById("chatHistory");

        const empty = history.querySelector(".empty");

        if (empty) {
            empty.remove();
        }


        const userMessage = document.createElement("div");

        userMessage.className = "message user-message";

        userMessage.innerHTML =
            "<b>You:</b><br>" + question;


        history.appendChild(userMessage);


        const aiMessage = document.createElement("div");

        aiMessage.className = "message ai-message";

        aiMessage.innerHTML =
            "<b>🤖 ShopEase AI:</b><br>" + answer;


        if (escalate) {

            aiMessage.innerHTML += `

                <div class="escalation">

                    ⚠️ This question needs to be handled
                    by human customer support.

                    <br>

                    <button class="support-btn"
                        onclick="contactSupport()">
                        👩‍💼 Contact Human Support
                    </button>

                </div>

            `;

        }


        aiMessage.innerHTML += `

            <div class="feedback">

                <button onclick="feedback('positive')">
                    👍 Helpful
                </button>

                <button onclick="feedback('negative')">
                    👎 Not Helpful
                </button>

            </div>

        `;


        history.appendChild(aiMessage);

        history.scrollTop = history.scrollHeight;

    }


    async function askAI() {

        const question =
            document.getElementById("question").value.trim();


        if (!question) {

            alert("Please enter a question.");

            return;

        }


        const history =
            document.getElementById("chatHistory");


        const empty =
            history.querySelector(".empty");


        if (empty) {
            empty.remove();
        }


        const loading =
            document.createElement("div");


        loading.className = "message ai-message";


        loading.innerHTML = `

            <div class="loading">

                <span>🤖 AI is thinking</span>

                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>

            </div>

        `;


        history.appendChild(loading);


        try {

            const response = await fetch("/ask", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })

            });


            const data = await response.json();


            loading.remove();


            addMessage(
                question,
                data.answer,
                data.escalate
            );


            chatHistory.push({
                question: question,
                answer: data.answer,
                escalate: data.escalate
            });


            document.getElementById("question").value = "";


        } catch (error) {

            loading.remove();

            addMessage(
                question,
                "Sorry, something went wrong. Please try again.",
                true
            );

        }

    }


    function feedback(type) {

        if (type === "positive") {

            alert("Thank you! 👍 Your feedback was recorded.");

        } else {

            alert("Thank you for your feedback. We will improve our support.");

        }

    }


    function contactSupport() {

        alert(
            "Human customer support is available Monday to Friday, 9 AM to 6 PM."
        );

    }


    document.getElementById("question").addEventListener(
        "keydown",
        function(event) {

            if (event.key === "Enter" && !event.shiftKey) {

                event.preventDefault();

                askAI();

            }

        }
    );

</script>

</body>

</html>
"""


@app.post("/ask")
def ask_question(data: Question):

    question = data.question.strip()

    results = search_knowledge(question)

    if not results:

        return {
            "answer": (
                "I don't have enough information in the "
                "ShopEase knowledge base to answer this question."
            ),
            "escalate": True
        }

    context = "\n\n".join(results)

    prompt = f"""
You are ShopEase AI, a strict e-commerce customer support assistant.

IMPORTANT RULES:

1. Answer ONLY using the information in the Knowledge Base.
2. NEVER use your general knowledge.
3. NEVER guess.
4. NEVER invent information.
5. NEVER assume something is true.
6. If the Knowledge Base does not clearly answer the question,
   say that the information is not available.
7. If the information is not available, the question must be
   escalated to human customer support.
8. If the Knowledge Base clearly answers the question,
   give a short and helpful answer.
9. Do not add information that is not present in the Knowledge Base.

KNOWLEDGE BASE:

{context}

CUSTOMER QUESTION:

{question}

Answer ONLY using the Knowledge Base.
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict customer support assistant. "
                    "Only use the provided knowledge base. "
                    "Never guess or invent information."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]

    escalation_words = [
        "not available",
        "not mentioned",
        "not provided",
        "not specified",
        "don't have enough information",
        "do not have enough information",
        "human customer support",
        "needs to be escalated",
        "escalate"
    ]

    escalate = any(
        word in answer.lower()
        for word in escalation_words
    )

    return {
        "answer": answer,
        "escalate": escalate
    }