from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

response = client.responses.create(
    model="gpt-5",
    input="""
Rewrite this into natural English:

Shen Jiyao was lying on the simple house designed by himself.
He squinted his eyes and frowned.
"""
)

print(type(response))
print()
print(response)