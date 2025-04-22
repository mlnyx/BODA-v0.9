import React from "react";

interface SummaryProps {
  data: {
    [metric: string]: {
      mean: number;
      median: number;
    };
  };
}

export default function ResultSummary({ data }: SummaryProps) {
  return (
    <section className="summary">
      <h2>요약 통계 (전체 평균 / 중앙값)</h2>
      <div className="result-grid">
        {Object.entries(data).map(([key, value]) => (
          <div className="card" key={key}>
            <h3>{key.toUpperCase()}</h3>
            <p>평균: {value.mean}%</p>
            <p>중앙값: {value.median}%</p>
          </div>
        ))}
      </div>
    </section>
  );
}
