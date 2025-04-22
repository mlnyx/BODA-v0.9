import React, { useState } from "react";
import FileSelector from "./components/FileSelector";
import ResultSummary from "./components/ResultSummary";
import CategoryTable from "./components/CategoryTable";
import TopImageCard from "./components/TopImageCard";

export default function App() {
  const [result, setResult] = useState<any>(null);

  const handleSelect = (gt: string, pred: string) => {
    fetch(`http://localhost:5001/preview?gt=${gt}&pred=${pred}`)
      .then((res) => res.json())
      .then((data) => setResult(data));
  };

  return (
    <main className="main-container">
      <h1>BODA - AI 성능 분석기</h1>
      <FileSelector onSelect={handleSelect} />

      {result && (
        <>
          <ResultSummary data={result.summary} />
          <TopImageCard topImages={result.top_images} />
          <CategoryTable data={result.categories} />
        </>
      )}
    </main>
  );
}
