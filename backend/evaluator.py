
import os
import json
import numpy as np
from shapely.geometry import Polygon
from collections import defaultdict, Counter
import math

CATEGORY_MAP = {
    0: "background",
    1: "bone",
    2: "enamel",
    3: "dentinA",
    4: "Pulp",
    5: "gingiva",
    6: "restoration(레진, GI)l",
    7: "restoration(메탈,골드,아말감)",
    8: "implant fixture",
    9: "abutment",
    10: "C1-caries(severe)",
    11: "C2-caries(medium)",
    12: "C3-caries(low)",
    13: "calculus",
    14: "post(metal. fiber)",
    15: "periapical abscess",
    16: "cone cut",
    17: "중첩법랑질",
    18: "duble line bone",
    19: "GP cone",
    20: "void(엔도, 보철, 충전 결손부)",
    21: "dentinB",
    22: "제외영역"
}

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_exterior_coords(geom):
    if geom.geom_type == "Polygon":
        return geom.exterior.coords
    elif geom.geom_type == "MultiPolygon":
        largest = max(geom.geoms, key=lambda p: p.area)
        return largest.exterior.coords
    return []

def iou_score(coords1, coords2):
    try:
        p1 = Polygon(coords1)
        p2 = Polygon(coords2)
        if not p1.is_valid or not p2.is_valid:
            return 0.0
        inter = p1.intersection(p2).area
        union = p1.union(p2).area
        return inter / union if union != 0 else 0.0
    except:
        return 0.0

def clean_nan(obj):
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return 0.0
    return obj

def evaluate_detailed(gt_path, pred_path):
    gt_data = load_json(gt_path)
    pred_data = load_json(pred_path)
    gt = gt_data['annotations']
    pred = pred_data['annotations']
    image_map = {img['id']: img['file_name'] for img in gt_data.get('images', [])}

    cat_stats = defaultdict(lambda: {"iou": [], "tp": 0, "fp": 0, "fn": 0, "pixel_acc": []})
    image_iou = defaultdict(list)

    for gt_ann in gt:
        gt_cat = gt_ann['category_id']
        gt_poly = Polygon(np.array(gt_ann['segmentation'][0]).reshape(-1, 2)).buffer(0)
        image_id = gt_ann['image_id']

        best_pred = None
        best_iou = 0
        for pred_ann in pred:
            if pred_ann['category_id'] != gt_cat:
                continue
            pred_poly = Polygon(np.array(pred_ann['segmentation'][0]).reshape(-1, 2)).buffer(0)
            iou = iou_score(get_exterior_coords(gt_poly), get_exterior_coords(pred_poly))
            if iou > best_iou:
                best_iou = iou
                best_pred = pred_poly

        cat_stats[gt_cat]['iou'].append(best_iou)
        cat_stats[gt_cat]['tp'] += int(best_iou >= 0.3)
        cat_stats[gt_cat]['fn'] += int(best_iou < 0.3)
        image_iou[image_id].append(best_iou)

        if best_iou >= 0.5 and best_pred:
            inter_area = gt_poly.intersection(best_pred).area
            pixel_acc = inter_area / gt_poly.area if gt_poly.area > 0 else 0
            cat_stats[gt_cat]['pixel_acc'].append(pixel_acc * 100)

    pred_counter = Counter([p['category_id'] for p in pred])
    for cat_id, counts in pred_counter.items():
        cat_stats[cat_id]['fp'] += counts

    category_result = {}
    for cat_id, stats in cat_stats.items():
        tp, fp, fn = stats['tp'], stats['fp'], stats['fn']
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        mean_iou = np.mean(stats['iou']) * 100 if stats['iou'] else 0.0
        pixel_acc = np.mean(stats['pixel_acc']) if stats['pixel_acc'] else 0.0
        label = CATEGORY_MAP.get(cat_id, f"Category {cat_id}")
        category_result[label] = {
            "precision": round(precision * 100, 1),
            "recall": round(recall * 100, 1),
            "f1_score": round(f1 * 100, 1),
            "iou": round(mean_iou, 1),
            "pixel_acc": round(pixel_acc, 1),
            "count": len(stats['iou'])
        }

    def extract_metric(metric):
        vals = [v[metric] for v in category_result.values() if v[metric] > 0]
        return round(np.mean(vals), 1), round(np.median(vals), 1)

    summary = {
        k: {
            "mean": extract_metric(k)[0],
            "median": extract_metric(k)[1]
        } for k in ["precision", "recall", "f1_score", "iou", "pixel_acc"]
    }

    avg_iou_per_img = [(image_map.get(k, f"id_{k}"), np.mean(v)) for k, v in image_iou.items() if len(v) > 0]
    top_images = sorted(avg_iou_per_img, key=lambda x: x[1], reverse=True)[:3]
    top_image_names = [name for name, _ in top_images]

    result = {
        "summary": summary,
        "categories": category_result,
        "top_images": top_image_names
    }

    return clean_nan(result)