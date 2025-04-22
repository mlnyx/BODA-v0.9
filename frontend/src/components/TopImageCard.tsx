import React from "react";

interface Props {
  topImages: string[];
}

export default function TopImageCard({ topImages }: Props) {
  return (
    <section>
      <h2>Top-3 이미지</h2>
      <div className="result-grid">
        {topImages.map((name, idx) => (
          <div className="card" key={idx}>
            <h3>TOP {idx + 1}</h3>
            <p>{name}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
