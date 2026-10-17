
from cap_931_sales_agent.llm_client import generate_response

# Test the shared local LLM function
prompt = (
    "You are a sales research assistant. "
    "In two sentences, explain why a sales representative "
    "should research a prospective company before a meeting."
)

answer = generate_response(prompt)

print("Local model response:")
print(answer)