import React from "react";

interface CategoryData {
  [label: string]: {
    precision: number;
    recall: number;
    f1_score: number;
    iou: number;
    pixel_acc: number;
    count: number;
  };
}

interface Props {
  data: CategoryData;
}

export default function CategoryTable({ data }: Props) {
  const sorted = Object.entries(data).sort((a, b) => b[1].iou - a[1].iou);

  return (
    <section>
      <h2>카테고리별 성능</h2>
      <table>
        <thead>
          <tr>
            <th>카테고리</th>
            <th>IoU (%)</th>
            <th>Precision</th>
            <th>Recall</th>
            <th>F1-Score</th>
            <th>Pixel Acc</th>
            <th>탐지 개수</th>
          </tr>
        </thead>
        <tbody>
          {sorted.map(([label, value]) => (
            <tr key={label}>
              <td>{label}</td>
              <td>{value.iou}</td>
              <td>{value.precision}</td>
              <td>{value.recall}</td>
              <td>{value.f1_score}</td>
              <td>{value.pixel_acc}</td>
              <td>{value.count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
