from openai import OpenAI
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
from dateutil import parser

load_dotenv()


def preprocess_reviews(path='./res/reviews.json'):
    with open(path, 'r', encoding='utf-8') as f:
        reviews = json.load(f)

    # 좋은 리뷰와 나쁜 리뷰 분리
    reviews_good, reviews_bad = [], []

    current_date = datetime.now()

    # 최근 6개월 이내의 리뷰만 추출
    date_boundary = current_date - timedelta(days=6*30)

    for review in reviews:
        review_date_str = review['date']
        try:
            # 리뷰 날짜 파싱
            review_date = parser.parse(review_date_str)
        except (ValueError, TypeError):
            # 날짜 파싱 실패 시 최근 날짜로 설정
            # 어차피 최근 6개월 이내의 리뷰만 추출하기 때문에 최근 날짜로 설정
            review_date = current_date

        if review_date < date_boundary:
            continue

        # 좋은 리뷰와 나쁜 리뷰 분리
        if review['star_count'] == 5:
            reviews_good.append(review['review_text'])
        else:
            reviews_bad.append(review['review_text'])

    # 좋은 리뷰와 나쁜 리뷰 텍스트 조합
    reviews_good_text = '\n'.join(reviews_good)
    reviews_bad_text = '\n'.join(reviews_bad)

    return reviews_good_text, reviews_bad_text
