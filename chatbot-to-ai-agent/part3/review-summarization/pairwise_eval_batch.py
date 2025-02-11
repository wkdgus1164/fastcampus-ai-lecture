from tqdm import tqdm
from pairwire_eval import pairwire_eval
from model import summarize_reviews


def pairwise_eval_batch(reviews, answers_a, answers_b):
    a_count = 0
    b_count = 0
    c_count = 0

    for i in tqdm(range(len(reviews))):
        result = pairwire_eval(reviews[i], answers_a[i], answers_b[i])
        verdict = result.choices[0].message.content

        if verdict == "[[A]]":
            a_count += 1
        elif verdict == "[[B]]":
            b_count += 1
        elif verdict == "[[C]]":
            c_count += 1
        else:
            print(f"Unexpected verdict: {verdict}")

    return a_count, b_count, c_count
