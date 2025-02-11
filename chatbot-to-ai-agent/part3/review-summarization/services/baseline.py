from openai import OpenAI
from dotenv import load_dotenv
from services.preprocess import preprocess


load_dotenv()
client = OpenAI()

PROMPT_BASELINE = """아래 숙소 리뷰에 대해 5문장 내로 요약해줘."""

reviews_good, reviews_bad = preprocess(path='./res/reviews.json')


def summarize(reviews, prompt=PROMPT_BASELINE):
    prompt = prompt + '\n\n' + reviews

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    return response.choices[0].message.content