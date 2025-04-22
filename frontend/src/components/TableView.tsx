import React from "react";

type Props = {
  data: Record<string, { mean_iou: number; count: number }>;
};

export default function TableView({ data }: Props) {
  return (
    <section>
      <h2>카테고리 상세 분석</h2>
      <table>
        <thead>
          <tr>
            <th>카테고리</th>
            <th>평균 IoU (%)</th>
            <th>탐지 개수</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(data).map(([key, value]) => (
            <tr key={key}>
              <td>{key}</td>
              <td>{value.mean_iou}</td>
              <td>{value.count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
