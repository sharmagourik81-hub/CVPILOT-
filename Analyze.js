import { useNavigate, useLocation } from "react-router-dom";
import { useState } from "react";
import axios from "axios";

function Analyze() {
  const nav = useNavigate();
  const { state } = useLocation();
  const [job, setJob] = useState("");

  const handleAnalyze = async () => {
    const formData = new FormData();
    formData.append("file", state.file);
    formData.append("job_description", job);

    const res = await axios.post("http://127.0.0.1:8000/analyze", formData);

    nav("/result", { state: res.data });
  };

  return (
    <div className="page">
      <div className="card">

        <h2>Job Description</h2>

        <textarea
          placeholder="Paste job description..."
          onChange={(e)=>setJob(e.target.value)}
        />

        <button onClick={handleAnalyze}>
          Analyze Resume
        </button>

      </div>
    </div>
  );
}

export default Analyze;