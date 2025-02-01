from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()

completion = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {
            'role': 'user',
            'content': '왜 하늘은 파란색인가요?'
        }
    ],
    temperature=1.0
)

print(completion.choices[0].message.content)
