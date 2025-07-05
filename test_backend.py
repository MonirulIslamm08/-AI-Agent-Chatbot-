from ai_agent import get_response_from_ai_agent

response = get_response_from_ai_agent(
    llm_id="gpt-4o-mini",
    query=["What is the capital of Bangladesh?"],
    allow_search=False,
    system_prompt="You are a helpful assistant.",
    provider="OpenAI"  
)

print(response)
