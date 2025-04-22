import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

type Props = {
  data: Record<string, { mean_iou: number }>;
};

export default function ChartView({ data }: Props) {
  const chartData = Object.entries(data).map(([label, value]) => ({
    category: label,
    mean_iou: value.mean_iou,
  }));

  return (
    <section>
      <h2>카테고리별 평균 IoU</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} layout="vertical">
          <XAxis type="number" domain={[0, 100]} hide />
          <YAxis dataKey="category" type="category" width={100} />
          <Tooltip formatter={(v: any) => `${v}%`} />
          <Bar dataKey="mean_iou" fill="#2f80ed" />
        </BarChart>
      </ResponsiveContainer>
    </section>
  );
}
