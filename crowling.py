from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#  selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver
# selenium으로 무엇인가 입력하기 위한 import
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd
'''
    패키지 모음
'''

options = Options()

options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(options=options)

url = "https://www.oliveyoung.co.kr/store/display/getCategoryShop.do?dispCatNo=10000010011&gateCd=Drawer&t_page=%EB%93%9C%EB%A1%9C%EC%9A%B0_%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC&t_click=%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC%ED%83%AD_%EB%8C%80%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC&t_1st_category_type=%EB%8C%80_%EC%84%A0%EC%BC%80%EC%96%B4"
#크롬 드라이버에 url 주소 넣고 실행
driver.get(url)

# 페이지가 완전히 로딩되도록 3초동안 기다림
time.sleep(3)

# ── 선케어에 맞게 수정된 선택자 ──────────────────────────────
# ❌ brand_selector 없음 (선케어 HTML에 tx_brand 태그 자체가 없어)
name_selector  = "a.prd_info > div.prd_name > p.tx_name"
price_selector = "a.prd_info > p.prd_price > span.tx_cur > span.tx_num"
url_selector   = "a.prd_info"

cosmetic = driver.find_elements(By.CSS_SELECTOR, name_selector)
price    = driver.find_elements(By.CSS_SELECTOR, price_selector)
url      = driver.find_elements(By.CSS_SELECTOR, url_selector)

print(f"상품명 {len(cosmetic)}개 / 가격 {len(price)}개 / URL {len(url)}개")

results = []
for (c, p, u) in zip(cosmetic, price, url):
    c_text = c.text
    p_text = p.text
    u_text = u.get_attribute("href")
    results.append({
        '이름': c_text,
        '가격': p_text.replace(",", ""),
        'url':  u_text
    })

df = pd.DataFrame(results)
print(df)

driver.quit()