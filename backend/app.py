from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from evaluator import evaluate_detailed
import os
import shutil

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
GT_DIR = os.path.join(BASE_DIR, "data", "GT")
AI_DIR = os.path.join(BASE_DIR, "data", "AI")

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/files")
def list_files():
    gt_files = os.listdir(GT_DIR)
    ai_files = os.listdir(AI_DIR)
    return {"gt": gt_files, "ai": ai_files}

@app.post("/analyze")
async def analyze_files(gt: UploadFile = File(...), pred: UploadFile = File(...)):
    gt_path = os.path.join(UPLOAD_DIR, gt.filename)
    pred_path = os.path.join(UPLOAD_DIR, pred.filename)
    with open(gt_path, "wb") as f:
        shutil.copyfileobj(gt.file, f)
    with open(pred_path, "wb") as f:
        shutil.copyfileobj(pred.file, f)

    result = evaluate_detailed(gt_path, pred_path)
    return JSONResponse(content=result)

@app.get("/preview")
def analyze_from_disk(gt: str, pred: str):
    gt_path = os.path.join(GT_DIR, gt)
    pred_path = os.path.join(AI_DIR, pred)
    if not os.path.exists(gt_path) or not os.path.exists(pred_path):
        return JSONResponse(status_code=404, content={"error": "파일이 존재하지 않습니다."})
    result = evaluate_detailed(gt_path, pred_path)
    return JSONResponse(content=result)