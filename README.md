# 🦷 BODA: 치과 영상 AI 분석 웹앱

**BODA(Bitewing Oral Diagnosis Assistant)**는 AI가 자동 분석한 치과 X-ray segmentation 결과를 수작업 Ground Truth(GT)와 비교하여 정량적 성능 분석을 제공하는 웹 기반 시스템입니다.
카테고리별 성능 지표, 전체 요약 통계, Top-N 이미지 시각화를 통해 진단 정확도를 한눈에 확인할 수 있습니다.

## 1. 기술 스택

Frontend: React + Vite + Tailwind CSS + Recharts (수평 막대그래프)

Backend: FastAPI + Shapely + NumPy + Scikit-learn

## 2. 주요 기능

📂 GT & AI 예측 JSON 파일 선택 후 자동 분석

📊 전체 성능 요약:

Precision, Recall, F1-score, IoU, Pixel Accuracy (평균 & 중앙값)

🗂 카테고리별 성능 테이블

각 클래스의 IoU, Precision, Recall, F1-score, 픽셀 정확도, 탐지 개수 제공

🥇 Top-3 이미지

AI 분석이 가장 잘 수행된 상위 3장 자동 추출

📈 수평 막대그래프 기반 직관적인 시각화

⏳ 분석 중 로딩 애니메이션, 결과 강조 색상 등 트렌디한 UI 반영

## 3. 설치 및 실행 방법

**백엔드 실행**
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 5001

**프론트엔드 실행**
cd frontend
npm install
npm run dev

## 4. 데이터 포맷 예시

JSON 형식: CVAT에서 export한 COCO-style 또는 polygon 기반 segmentation

필수 구조:

{
"annotations": [
{
"image_id": 1,
"category_id": 3,
"segmentation": [[...]]
}
],
"images": [
{
"id": 1,
"file_name": "example.tif"
}
]
}
