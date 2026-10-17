import os

from dotenv import load_dotenv
from openai import OpenAI

# Load variables from the .env file
load_dotenv()

# Create the OpenAI client using OPENAI_API_KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Send a simple test request
response = client.responses.create(
    model="gpt-6-luna",
    input="Respond with exactly: CAP 931 GPT connection successful."
)

print(response.output_text)