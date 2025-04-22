import React, { useEffect, useState } from "react";

export default function FileList() {
  const [files, setFiles] = useState<string[]>([]);

  useEffect(() => {
    fetch("http://localhost:5001/files")
      .then((res) => res.json())
      .then((data) => setFiles(data.files));
  }, []);

  return (
    <section>
      <h2>업로드된 파일</h2>
      <ul>
        {files.map((file, idx) => (
          <li key={idx}>{file}</li>
        ))}
      </ul>
    </section>
  );
}
