import json
from datetime import datetime, timedelta
from dateutil import parser


def preprocess(path='./res/reviews.json') -> tuple[str, str]:
    """
    리뷰 데이터를 전처리하는 함수
    """
    with open(path, 'r', encoding='utf-8') as f:
        reviews = json.load(f)

    reviews_good, reviews_bad = [], []

    current_date = datetime.now()
    date_boundry = current_date - timedelta(days=6*30)

    for review in reviews:
        review_date_str = review['date']

        try:
            review_date = parser.parse(review_date_str)
        except (ValueError, TypeError):
            review_date = current_date

        if review_date > date_boundry:
            continue

        if review['star_count'] >= 4:
            reviews_good.append(
                '[REVIEW_START] ' + review['review_text'] + '[REVIEW_END]'
            )
        else:
            reviews_bad.append(
                '[REVIEW_START] ' + review['review_text'] + '[REVIEW_END]'
            )

    reviews_good_text = '\n'.join(reviews_good)
    reviews_bad_text = '\n'.join(reviews_bad)

    return reviews_good_text, reviews_bad_text


if __name__ == '__main__':
    reviews_good, reviews_bad = preprocess()
