from dotenv import load_dotenv
from services.preprocess import preprocess
from services.baseline import summarize
from services.pairwise_eval import pairwise_eval

load_dotenv()

# 1. 리뷰 크롤링
# reviews = crawl_reviews()
# print(reviews)

# 2. 리뷰 전처리
reviews_good, reviews_bad = preprocess(path='./res/reviews.json')

# 3. 리뷰 요약 및 평가
print(summarize(reviews_good))

# 4. 페어와이즈 평가
print(
    pairwise_eval(
        reviews_good,
        summarize(reviews_good),
        summarize(reviews_bad)
    )
)