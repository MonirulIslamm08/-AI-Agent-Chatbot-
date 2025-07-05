from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import requests
import json
from datetime import datetime
import uuid

st.set_page_config(
    page_title="Agent Studio",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    body {
        font-family: "Segoe UI", sans-serif;
    }
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .message-user, .message-assistant {
        border-left: 4px solid #ccc;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: #f9f9f9;
    }
    .message-assistant {
        border-left-color: #007bff;
    }
    .message-header {
        font-size: 0.8rem;
        font-weight: bold;
        color: #555;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
    }
    .message-content {
        font-size: 0.95rem;
        color: #212529;
    }
</style>
""", unsafe_allow_html=True)

if 'conversations' not in st.session_state:
    st.session_state.conversations = {}
if 'current_conversation_id' not in st.session_state:
    st.session_state.current_conversation_id = None
if 'chain_mode' not in st.session_state:
    st.session_state.chain_mode = False
if 'query_counter' not in st.session_state:
    st.session_state.query_counter = 0

MODELS = {
    "Groq": ["llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile"],
    "OpenAI": ["gpt-4o", "gpt-3.5-turbo"]
}

TEMPLATES = {
    "Research Analyst": {"system_prompt": "Act as a research analyst."},
    "Content Strategist": {"system_prompt": "Act as a content strategist."},
    "Custom Agent": {"system_prompt": "You are a helpful AI assistant."},
    "Financial Advisor": {"system_prompt": "Act as a financial advisor."},
    "Marketing Specialist": {"system_prompt": "Act as a marketing expert."}
}

API_URL = "http://127.0.0.1:9999/chat"

def create_conversation_id():
    return str(uuid.uuid4())[:8]

def save_message(conv_id, role, content, model_info):
    if conv_id not in st.session_state.conversations:
        title = content[:50] + "..." if len(content) > 50 else content
        st.session_state.conversations[conv_id] = {
            "title": title,
            "messages": [],
            "created_at": datetime.now(),
            "model_info": model_info
        }
    st.session_state.conversations[conv_id]["messages"].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now()
    })

def get_agent_response(payload):
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        data = response.json()
        if response.status_code == 200:
            return data if isinstance(data, str) else json.dumps(data)
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"

# Sidebar
with st.sidebar:
    st.subheader("Agent Settings")
    selected_template = st.selectbox("Template", list(TEMPLATES.keys()))
    provider = st.radio("Provider", list(MODELS.keys()))
    selected_model = st.selectbox("Model", MODELS[provider])
    allow_web_search = st.checkbox("Web Search", value=False)
    st.session_state.chain_mode = st.checkbox("Chain Queries", value=st.session_state.chain_mode)

    st.markdown("---")
    st.subheader("Conversations")
    if st.session_state.conversations:
        for conv_id, conv in reversed(list(st.session_state.conversations.items())):
            if st.button(conv['title'], key=f"load_{conv_id}"):
                st.session_state.current_conversation_id = conv_id
                st.rerun()
    else:
        st.caption("No conversations yet.")

    if st.button("New Chat"):
        st.session_state.current_conversation_id = None
        st.rerun()
    if st.button("Clear All"):
        st.session_state.conversations.clear()
        st.rerun()

# Main Header
st.markdown('<div class="main-header">Agent Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI assistant for focused productivity</div>', unsafe_allow_html=True)

try:
    health = requests.get("http://127.0.0.1:9999/health", timeout=5)
    status = "Online" if health.status_code == 200 else "Offline"
except:
    status = "Offline"

st.caption(f"Backend Status: {status} | Model: {selected_model} | Provider: {provider}")

# Show conversation
if st.session_state.current_conversation_id:
    conv = st.session_state.conversations[st.session_state.current_conversation_id]
    st.markdown(f"**Conversation:** {conv['title']}")
    for msg in conv["messages"]:
        css_class = "message-user" if msg["role"] == "user" else "message-assistant"
        role_label = "User" if msg["role"] == "user" else "Assistant"
        st.markdown(f"""
        <div class="{css_class}">
            <div class="message-header">{role_label}</div>
            <div class="message-content">{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)

# Query input
st.subheader("Enter Query")
current_query_key = f"user_query_{st.session_state.query_counter}"
user_query = st.text_area("Your message", height=100, key=current_query_key)

col1, col2 = st.columns([2, 1])

with col1:
    if st.button("Send"):
        if user_query.strip():
            if not st.session_state.current_conversation_id:
                st.session_state.current_conversation_id = create_conversation_id()
            messages = [user_query]
            if st.session_state.chain_mode:
                conv = st.session_state.conversations.get(st.session_state.current_conversation_id, {})
                history = conv.get("messages", [])[-4:]
                context = "\n".join([f"{m['role']}: {m['content']}" for m in history])
                messages = [f"Previous context:\n{context}\n\nCurrent query: {user_query}"]
            payload = {
                "model_name": selected_model,
                "model_provider": provider,
                "system_prompt": TEMPLATES[selected_template]["system_prompt"],
                "messages": messages,
                "allow_search": allow_web_search
            }
            model_info = {
                "model": selected_model,
                "provider": provider,
                "search_enabled": allow_web_search,
                "template": selected_template
            }
            save_message(st.session_state.current_conversation_id, "user", user_query, model_info)
            with st.spinner("Processing..."):
                response = get_agent_response(payload)
            save_message(st.session_state.current_conversation_id, "assistant", response, model_info)
            st.session_state.query_counter += 1
            st.rerun()
        else:
            st.warning("Please enter a query.")

with col2:
    if st.button("Export"):
        export_data = {
            "conversations": {
                k: {
                    **v,
                    "created_at": v["created_at"].isoformat(),
                    "messages": [
                        {**m, "timestamp": m["timestamp"].isoformat()} for m in v["messages"]
                    ]
                } for k, v in st.session_state.conversations.items()
            },
            "exported_at": datetime.now().isoformat()
        }
        st.download_button(
            label="Download JSON",
            data=json.dumps(export_data, indent=2),
            file_name=f"agent_conversations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

st.markdown("---")
st.caption(f"{len(st.session_state.conversations)} conversations | Total messages: {sum(len(c['messages']) for c in st.session_state.conversations.values())}")