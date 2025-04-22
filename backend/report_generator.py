import os
from evaluator import evaluate_detailed
from datetime import datetime

def generate_html_report(gt_path, pred_path):
    result = evaluate_detailed(gt_path, pred_path)
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    report_path = os.path.join("backend/uploads", filename)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"""
        <html>
        <head><meta charset='utf-8'><title>BODA 리포트</title></head>
        <body style='font-family: sans-serif;'>
        <h1>📊 BODA 분석 리포트</h1>
        <h2>요약 결과</h2>
        <ul>
        {''.join([f'<li><b>{k}:</b> {v}%</li>' for k, v in result['overall'].items()])}
        </ul>
        <h2>카테고리별 상세</h2>
        <table border='1' cellpadding='8'><tr><th>카테고리</th><th>평균 IoU</th><th>탐지 개수</th></tr>
        {''.join([f'<tr><td>{k}</td><td>{v["mean_iou"]}</td><td>{v["count"]}</td></tr>' for k,v in result['categories'].items()])}
        </table>
        </body></html>
        """)
    return report_path
