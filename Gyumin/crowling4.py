from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from pyshadow.main import Shadow
import sqlite3

# ── 드라이버 세팅 ─────────────────────────────────────────────
options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# ── DB 세팅 ──────────────────────────────────────────────────
conn = sqlite3.connect("oliveyoung_reviews.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id   TEXT,
    product_name TEXT,
    author       TEXT,
    skin_type    TEXT,
    rating       INTEGER,
    review_date  TEXT,
    option       TEXT,
    review_text  TEXT,
    is_fake      INTEGER DEFAULT 0
)
""")
conn.commit()

BATCH_SIZE = 100  # 몇 개마다 DB에 저장할지

def save_batch(conn, product_id, product_name, name_list, skin_list, star_list,
               date_list, good_list, text_list, already_saved_count):
    """already_saved_count 이후의 새 항목만 DB에 저장"""
    saved = 0
    for i in range(already_saved_count, len(name_list)):
        conn.execute("""
            INSERT INTO reviews
            (product_id, product_name, author, skin_type, rating, review_date, option, review_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            product_id, product_name,
            name_list[i], skin_list[i], star_list[i],
            date_list[i], good_list[i], text_list[i]
        ))
        saved += 1
    conn.commit()
    return saved

# ── 무한스크롤 리뷰 수집 함수 ─────────────────────────────────
def scroll_and_crawl(driver, product_id, product_name, target_count=10000):
    name_list, skin_list, star_list = [], [], []
    date_list, good_list, text_list = [], [], []

    # 재시작 시 이미 DB에 있는 리뷰 텍스트 로드 → 중복 방지
    existing = set(
        row[0] for row in conn.execute(
            "SELECT review_text FROM reviews WHERE product_id = ?", (product_id,)
        )
    )
    collected_reviews = set(existing)
    print(f"기존 DB에 저장된 리뷰: {len(existing)}개 (중복 스킵 적용)")

    no_new_count = 0
    last_saved_index = 0
    total_db_saved = 0

    while len(name_list) < target_count:
        try:
            shadow = Shadow(driver)
            users = shadow.find_elements('div.inner')
        except Exception as e:
            print(f"Shadow DOM 접근 실패, 재시도: {e}")
            time.sleep(3)
            continue

        initial_count = len(name_list)

        for user in users:
            try:
                user_hosts = user.find_elements(By.CSS_SELECTOR, 'oy-review-review-user')
                text_hosts = user.find_elements(By.CSS_SELECTOR, 'oy-review-review-content')

                if not user_hosts or not text_hosts:
                    continue

                # 리뷰 본문
                text_shadow = text_hosts[0].shadow_root
                t_el = text_shadow.find_elements(By.CSS_SELECTOR, 'div.content')
                if not t_el:
                    t_el = text_shadow.find_elements(By.CSS_SELECTOR, 'p')
                review_text = t_el[0].text.strip() if t_el else ""

                if not review_text or review_text in collected_reviews:
                    continue

                # 날짜
                date = user.find_elements(By.CSS_SELECTOR, 'div.common-info span.date')
                date_text = date[0].text if date else None

                # 유저 정보
                user_shadow = user_hosts[0].shadow_root
                n_el = user_shadow.find_elements(By.CSS_SELECTOR, 'div.info div.name')
                s_el = user_shadow.find_elements(By.CSS_SELECTOR, 'div.info div.skin-types')
                star_rating = user.find_elements(By.CSS_SELECTOR, "div.meta div.rating oy-review-star-icon")
                goods_option = user.find_elements(By.CSS_SELECTOR, 'div.goods-option')

                name_list.append(n_el[0].text if n_el else "이름없음")
                skin_list.append(s_el[0].text.replace('\n', ',') if s_el else None)
                star_list.append(len(star_rating))
                date_list.append(date_text)
                good_list.append(goods_option[0].text if goods_option else None)
                text_list.append(review_text.replace('\n', ' '))
                collected_reviews.add(review_text)

                if len(name_list) >= target_count:
                    break

            except Exception:
                continue

        # ── 배치 저장 ─────────────────────────────────────────
        if len(name_list) - last_saved_index >= BATCH_SIZE:
            saved = save_batch(conn, product_id, product_name,
                               name_list, skin_list, star_list,
                               date_list, good_list, text_list,
                               last_saved_index)
            total_db_saved += saved
            last_saved_index = len(name_list)
            print(f"💾 배치 저장: +{saved}개 (누적 DB: {total_db_saved}개)")

        # 스크롤
        driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(4)

        if len(name_list) == initial_count:
            no_new_count += 1
            print(f"새로운 리뷰 로딩 대기 중... ({no_new_count}/7)")
        else:
            no_new_count = 0

        if no_new_count >= 7:
            print("더 이상 불러올 리뷰가 없어 수집을 종료합니다.")
            break

        print(f"현재 수집된 리뷰: {len(name_list)}개...")

    # ── 나머지 저장 ───────────────────────────────────────────
    saved = save_batch(conn, product_id, product_name,
                       name_list, skin_list, star_list,
                       date_list, good_list, text_list,
                       last_saved_index)
    total_db_saved += saved
    print(f"✅ 수집 완료: 전체 {len(name_list)}개 수집 / DB 저장 {total_db_saved}개 (2022년 이전)")

    return name_list, skin_list, star_list, date_list, good_list, text_list

# ── 실행 ─────────────────────────────────────────────────────
URL = "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000223906"
PRODUCT_ID = "A000000223906"
PRODUCT_NAME = "식물나라 수분 선젤"

driver.get(URL)
time.sleep(5)

# 리뷰 탭 자동 클릭
for xpath in ["//button[contains(text(), '리뷰')]", "//a[contains(text(), '리뷰')]"]:
    try:
        el = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].click();", el)
        print("✅ 리뷰탭 클릭 성공")
        break
    except:
        continue

time.sleep(3)
driver.execute_script('window.scrollBy(0, 3000);')
time.sleep(3)

# 수집 실행
names, skins, stars, dates, options, texts = scroll_and_crawl(
    driver, PRODUCT_ID, PRODUCT_NAME, target_count=10000
)

# 결과 확인
df = pd.DataFrame({
    '작성자': names, '피부타입': skins, '별점': stars,
    '날짜': dates, '옵션': options, '본문': texts
})
print(df)
print(f"\n총 {len(df)}개 수집 완료")

driver.quit()
conn.close()
