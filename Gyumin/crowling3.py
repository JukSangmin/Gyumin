from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyshadow.main import Shadow
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

# 리뷰 탭 클릭
for xpath in ["//button[contains(text(), '리뷰')]", "//a[contains(text(), '리뷰')]"]:
    try:
        el = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].click();", el)
        print(f"✅ 리뷰탭 클릭 성공")
        break
    except:
        continue

time.sleep(3)

# 스크롤 내려서 리뷰 로딩
driver.execute_script('window.scrollBy(0, 3000);')
time.sleep(3)

import pandas as pd

shadow = Shadow(driver)

all_names = []
all_dates = []
all_options = []
all_texts = []

prev_count = 0

while True:
    # 현재 페이지 데이터 수집
    names = [n.text for n in shadow.find_elements('div.inner oy-review-review-user div.info div.name')]
    dates = [d.text for d in shadow.find_elements('div.inner div.common-info span.date')]
    options = [o.text for o in shadow.find_elements('div.inner div.goods-option')]
    texts = [r.text for r in shadow.find_elements('oy-review-review-content p')]

    # 2022-12-31 이전 날짜 있는지 체크
    has_old = any(d <= '2022.12.31' for d in dates)

    # 데이터 추가
    for i in range(len(names)):
        if dates[i] <= '2022.12.31':  # 날짜 필터
            all_names.append(names[i])
            all_dates.append(dates[i])
            all_options.append(options[i])
            all_texts.append(texts[i])

    print(f"현재 {len(names)}개 로드됨 / 2022년 이전 수집: {len(all_names)}개")

    # 2022년 이전 데이터 나오면 중단
    if has_old:
        print("2022년 이전 리뷰 발견 → 수집 완료")
        break

    # 스크롤 더 내리기
    driver.execute_script('window.scrollBy(0, 2000);')
    time.sleep(3)

    # 새로 로드된 게 없으면 중단 (마지막 페이지)
    new_count = len(names)
    if new_count == prev_count:
        print("더 이상 리뷰 없음 → 종료")
        break
    prev_count = new_count

df = pd.DataFrame({
    '작성자': all_names,
    '날짜': all_dates,
    '옵션': all_options,
    '본문': all_texts,
})

print(f"총 수집: {len(df)}개")
print(df)
driver.quit()