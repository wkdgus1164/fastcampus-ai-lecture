import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver

URL = "https://www.yanolja.com/reviews/domestic/1000086255?sort=HOST_CHOICE"

SCROLL_SCRIPT = "window.scrollTo(0, document.body.scrollHeight);"
REVIEW_ITEM_SELECTOR = 'div.review-item-container'
REVIEW_DATE_SELECTOR = f'{REVIEW_ITEM_SELECTOR} .css-1ivchjf p.css-1irbwe1'
REVIEW_TEXT_SELECTOR = 'content-text'

# 웹 드라이버 초기화
driver = webdriver.Chrome()


def crawl_reviews() -> tuple[str, str]:
    """
    리뷰 데이터를 크롤링하여 추출하는 함수

    동작 방식:

        1. 웹 드라이버를 초기화하고 대상 URL로 이동
        2. 페이지 로드 후 10번 스크롤 다운
        3. 리뷰 데이터를 파싱하여 리스트로 반환
        4. 리뷰 데이터를 JSON 파일로 저장
    """
    driver.get(URL)

    time.sleep(3)
    scroll_down(10)

    # 리뷰 데이터 파싱
    review_list = parse_reviews()

    # 리뷰 데이터 저장
    with open('./res/reviews.json', 'w', encoding='utf-8') as f:
        json.dump(
            review_list,
            f,
            ensure_ascii=False,
            indent=4
        )

    return review_list


def scroll_down(scroll_count: int) -> None:
    """
    웹페이지를 스크롤하여 추가 리뷰 데이터를 로드

    동작 방식:

        1. 지정된 횟수만큼 페이지 하단으로 스크롤
        2. 각 스크롤마다 2초간 대기하여 새로운 컨텐츠가 로드되도록 함
    """

    for i in range(scroll_count):
        driver.execute_script(SCROLL_SCRIPT)
        time.sleep(2)


def parse_reviews() -> tuple[str, str]:
    """
    리뷰 컨테이너와 리뷰 날짜를 파싱하여 리뷰 데이터를 추출
    """

    # 리뷰 데이터 리스트
    review_list = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 리뷰 컨테이너와 리뷰 날짜 추출
    review_containers = soup.select(REVIEW_ITEM_SELECTOR)
    review_date = soup.select(REVIEW_DATE_SELECTOR)

    for i in range(len(review_containers)):
        review_text = review_containers[i].find(
            'p',
            class_=REVIEW_TEXT_SELECTOR
        ).text

        review_stars = review_containers[i].find_all(
            'path', {
                'fill-rule': 'evenodd'
            }
        )

        star_count = 5 - len(review_stars)
        date = review_date[i].text

        review_dict = {
            'review_text': review_text,
            'star_count': star_count,
            'date': date
        }
        review_list.append(review_dict)

    return review_list


if __name__ == '__main__':
    crawl_reviews()
