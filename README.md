# BODA: 치과 영상 AI 분석 웹앱

AI가 자동 분석한 치과 X-ray segmentation 결과를 GT와 비교해 성능을 정량적으로 평가하는 웹 기반 시스템입니다.

## 🧩 기술 스택

- **Frontend**: React + Vite + Recharts (수평 막대그래프)
- **Backend**: FastAPI + Shapely + NumPy + Scikit-learn

## ✅ 지원 기능

- GT & 예측 JSON 파일 업로드 및 자동 분석
- 전체 정확도, F1-score, IoU, 픽셀 정확도 요약
- 카테고리별 IoU, 탐지 개수 테이블 제공
- 막대 그래프로 직관적인 시각화

## 📦 설치 및 실행

### 백엔드 실행

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 5001
```

### 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

## 📁 데이터 예시

- GT/AI JSON 형식은 CVAT에서 export한 COCO style 또는 polygon segmentation 형식 기준
- `annotations` 안에 `category_id` 및 `segmentation` 포함되어야 합니다.

## ✨ 향후 확장 가능

- Top-N 이미지 시각화 (탐지 잘된 이미지)
- HTML 리포트 PDF 자동 저장
- 여러 결과 비교 (히스토리 기능)
- 사용자 업로드 관리 시스템
