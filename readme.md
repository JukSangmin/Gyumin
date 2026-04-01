# 🌿 올리브영 선케어 리뷰 크롤러

올리브영 선케어 카테고리 상품의 리뷰를 수집하는 크롤러입니다.  
수집한 리뷰는 SQLite DB에 저장되며, 가짜 리뷰 탐지 연구에 활용됩니다.

---

## 📦 설치 방법 (처음 세팅하는 사람용)

### 1. 파이썬 설치
Python **3.14.2** 버전을 사용합니다.  
👉 https://www.python.org/downloads/ 에서 다운로드 후 설치

> ⚠️ 설치할 때 **"Add Python to PATH"** 체크박스 반드시 체크!

---

### 2. 레포지토리 클론
터미널(cmd 또는 Git Bash)을 열고 아래 명령어를 입력합니다.

```bash
git clone https://github.com/JukSangmin/Gyumin.git
cd Gyumin
```

---

### 3. 가상환경 만들기
가상환경은 이 프로젝트에서만 쓰는 독립적인 파이썬 환경입니다.  
다른 프로젝트랑 패키지가 섞이지 않게 해줘요.

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate
```

> ✅ 활성화되면 터미널 앞에 `(venv)` 표시가 생겨요!

---

### 4. 패키지 설치

```bash
pip install -r requirements.txt
```

> 이 명령어 하나로 필요한 패키지가 전부 설치됩니다.

---

### 5. 크롤러 실행

```bash
python crowling.py
```

> ⚠️ 실행하면 크롬 브라우저가 자동으로 열립니다. 건드리지 마세요!

---

## 📁 디렉토리 구조

```
Gyumin/
├── crowling.py          # 상품 목록 수집
├── crowling2.py         # Shadow DOM 테스트
├── crowling3.py         # 리뷰 수집 메인 코드
├── requirements.txt     # 패키지 목록
├── oliveyoung_reviews.db  # 수집된 리뷰 DB (실행 후 생성됨)
└── README.md
```

---

## 🗄️ DB 구조

수집된 리뷰는 `oliveyoung_reviews.db` 파일에 저장됩니다.

| 컬럼 | 설명 |
|---|---|
| product_id | 상품 고유 번호 |
| product_name | 상품명 |
| author | 작성자 닉네임 |
| skin_type | 피부타입 |
| rating | 별점 (1~5) |
| review_date | 작성 날짜 |
| option | 구매 옵션 |
| review_text | 리뷰 본문 |

---

## ⚙️ 환경

- Python 3.14.2
- Chrome 브라우저 필요 (자동으로 드라이버 설치됨)
- Windows / Mac / Linux 모두 가능