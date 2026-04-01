from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000223906")
time.sleep(5)

# oy- 로 시작하는 커스텀 요소 전부 찾기
oy_elements = driver.execute_script("""
    return Array.from(document.querySelectorAll('*'))
        .filter(el => el.tagName.toLowerCase().startsWith('oy-'))
        .map(el => el.tagName.toLowerCase());
""")

print("oy- 요소 목록:")
print(oy_elements)

# 리뷰 탭 클릭 후 아래 코드 추가
time.sleep(5)

# 1단계: 가장 바깥쪽 host 찾기
host1 = driver.find_element(By.CSS_SELECTOR, 'oy-review-review-in-product')
root1 = driver.execute_script('return arguments[0].shadowRoot', host1)
time.sleep(3)

els = root1.find_elements(By.CSS_SELECTOR, '*')
print([e.tag_name for e in els])


# 2단계: oy-review-review-overview 뚫기
host4 = root1.find_element(By.CSS_SELECTOR, 'oy-review-review-overview')
root4 = driver.execute_script('return arguments[0].shadowRoot', host4)
time.sleep(1)

els = root4.find_elements(By.CSS_SELECTOR, '*')
print([e.tag_name for e in els])

# 3단계: oy-review-review-overview-pc 뚫기
host5 = root4.find_element(By.CSS_SELECTOR, 'oy-review-review-overview-pc')
root5 = driver.execute_script('return arguments[0].shadowRoot', host5)
time.sleep(1)

els = root5.find_elements(By.CSS_SELECTOR, '*')
print([e.tag_name for e in els])

# 4단계: oy-review-star-rating 뚫기
host6 = root5.find_element(By.CSS_SELECTOR, 'oy-review-star-rating')
root6 = driver.execute_script('return arguments[0].shadowRoot', host6)
time.sleep(1)

els = root6.find_elements(By.CSS_SELECTOR, '*')
print([e.tag_name for e in els])

# 5단계: 평점 & 리뷰 수 추출
rating_score = root6.find_element(By.CSS_SELECTOR, '.rating-score').text
total_count = root6.find_element(By.CSS_SELECTOR, '.total-count').text

print(f"평점: {rating_score}, 리뷰수: {total_count}")

# oy-review-review-list 뚫기
host_list = root1.find_element(By.CSS_SELECTOR, 'oy-review-review-list')
root_list = driver.execute_script('return arguments[0].shadowRoot', host_list)
time.sleep(1)

els = root_list.find_elements(By.CSS_SELECTOR, '*')
print([e.tag_name for e in els])

# oy-review-review-item 첫 번째 하나만 뚫어보기
host_item = root_list.find_element(By.CSS_SELECTOR, 'oy-review-review-item')
root_item = driver.execute_script('return arguments[0].shadowRoot', host_item)
time.sleep(1)

els = root_item.find_elements(By.CSS_SELECTOR, '*')
print([e.tag_name for e in els])

# oy-review-review-content 뚫기
host_content = root_item.find_element(By.CSS_SELECTOR, 'oy-review-review-content')
root_content = driver.execute_script('return arguments[0].shadowRoot', host_content)
time.sleep(1)

els = root_content.find_elements(By.CSS_SELECTOR, '*')
print([e.tag_name for e in els])

# 리뷰 본문 텍스트 추출
review_text = root_content.find_element(By.CSS_SELECTOR, 'p').text
print(f"리뷰 본문: {review_text}")

# root_item에서 span 텍스트 확인
spans = root_item.find_elements(By.CSS_SELECTOR, 'span')
for span in spans:
    print(f"span: '{span.text}'")

input("확인 후 엔터")
driver.quit()