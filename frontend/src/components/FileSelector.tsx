import React, { useEffect, useState } from "react";

interface Props {
  onSelect: (gt: string, pred: string) => void;
}

export default function FileSelector({ onSelect }: Props) {
  const [gtFiles, setGtFiles] = useState<string[]>([]);
  const [aiFiles, setAiFiles] = useState<string[]>([]);
  const [gtSelected, setGtSelected] = useState<string>("");
  const [aiSelected, setAiSelected] = useState<string>("");

  useEffect(() => {
    fetch("http://localhost:5001/files")
      .then((res) => res.json())
      .then((data) => {
        setGtFiles(data.gt);
        setAiFiles(data.ai);
      });
  }, []);

  const handleAnalyze = () => {
    if (gtSelected && aiSelected) {
      onSelect(gtSelected, aiSelected);
    }
  };

  return (
    <div className="file-selector">
      <h3>분석할 파일 선택</h3>
      <div className="dropdowns">
        <div>
          <label>GT 파일</label>
          <select
            value={gtSelected}
            onChange={(e) => setGtSelected(e.target.value)}
          >
            <option value="">선택</option>
            {gtFiles.map((file, idx) => (
              <option key={idx} value={file}>
                {file}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>AI 예측 파일</label>
          <select
            value={aiSelected}
            onChange={(e) => setAiSelected(e.target.value)}
          >
            <option value="">선택</option>
            {aiFiles.map((file, idx) => (
              <option key={idx} value={file}>
                {file}
              </option>
            ))}
          </select>
        </div>
        <button onClick={handleAnalyze}>분석 시작</button>
      </div>
    </div>
  );
}
