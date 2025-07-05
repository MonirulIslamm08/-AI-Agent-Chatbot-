## 🧠 Personal Agentic AI Chatbot

This project is a multi-agent AI chatbot system using **LangGraph + LangChain**, featuring real-time web search via **Tavily**, model selection with **Groq** and **OpenAI**, and a user interface built with **Streamlit**.

### 🔧 Features

* 🔁 Supports **multiple LLM providers**: OpenAI (`gpt-4o-mini`) and Groq (`llama-3.3-70b-versatile`)
* 🌐 **Web search-enabled** via Tavily API
* 💬 Smart AI agents with **bullet-point summaries (< 80 words)**
* ⚡ Interactive **Streamlit frontend**
* 🛠️ **FastAPI backend** to serve agent logic
* 🧩 Modular structure (`ai_agent.py`, `backend.py`, `frontend.py`)

---

### 📁 Project Structure

```
📦 Personal_Agentic_AI_Chatbot/
│
├── ai_agent.py       # Agent logic (LangGraph + tools)
├── backend.py        # FastAPI backend server
├── frontend.py       # Streamlit user interface
├── requirements.txt  # Project dependencies
├── .env              # Environment variables for API keys (not tracked)
└── README.md         # You are here
```

---

### 🚀 How to Run

#### 1️⃣ Clone the repo

```bash
git clone  https://github.com/MonirulIslamm08/-AI-Agent-Chatbot-
cd Personal_Agentic_AI_Chatbot
```

#### 2️⃣ Set up a virtual environment

```bash
python -m venv myenv
source myenv/bin/activate  # or myenv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### 3️⃣ Create a `.env` file

```env
GROQ_API_KEY=your_groq_key_here
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
```

#### 4️⃣ Run the backend (FastAPI)

```bash
uvicorn backend:app --reload --port 9999
```

#### 5️⃣ Run the frontend (Streamlit)

In a new terminal:

```bash
streamlit run frontend.py
```

---

### 📸 Screenshot

> *(Optional: Add a screenshot of your Streamlit UI here)*

---

### ✅ Example Use

Ask:

> *"What are the latest trends in cryptocurrency?"*

Output:

```
1. Bitcoin surged 150% in 2024 after ETF approvals.
2. Crypto adoption increased via institutional investments.
3. CBDCs and regulations reshape global markets.
```

---

### 📦 Requirements

See `requirements.txt`. Key libraries:

* `langchain`
* `langgraph`
* `streamlit`
* `fastapi`
* `uvicorn`
* `tavily-python`
* `requests`


