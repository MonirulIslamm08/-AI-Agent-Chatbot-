# ai_agent.py

from dotenv import load_dotenv
load_dotenv()

import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage

# Step 1: Load API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Step 2: Default concise system prompt
DEFAULT_SYSTEM_PROMPT = (
    "You are a smart and friendly AI assistant. "
    "Answer all questions using 3–5 clear bullet points, under 80 words total."
)

# Step 3: AI Agent logic
def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    try:
        # Select model
        if provider == "Groq":
            llm = ChatGroq(model=llm_id, groq_api_key=GROQ_API_KEY)
        elif provider == "OpenAI":
            llm = ChatOpenAI(model=llm_id, api_key=OPENAI_API_KEY)
        else:
            return "❌ Invalid provider selected."

        tools = [TavilySearchResults(api_key=TAVILY_API_KEY, max_results=2)] if allow_search else []

        # Final prompt
        final_prompt = system_prompt.strip() or DEFAULT_SYSTEM_PROMPT

        # Create agent
        agent = create_react_agent(
            model=llm,
            tools=tools,
            state_modifier=final_prompt
        )

        # Convert last user message
        state = {"messages": [HumanMessage(content=query[-1])]}
        response = agent.invoke(state)

        # Extract response
        messages = response.get("messages", [])
        ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
        return ai_messages[-1] if ai_messages else "⚠️ No response from agent."
    except Exception as e:
        return f"🔥 Agent Error: {str(e)}"
