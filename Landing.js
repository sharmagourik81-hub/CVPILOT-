import { useNavigate } from "react-router-dom";

function Landing() {
  const nav = useNavigate();

  return (
    <div className="page">
      <div className="card">
        <h1>🚀 AI Resume Analyzer</h1>
        <p style={{marginTop:"10px"}}>Get ATS score & job match instantly</p>

        <button onClick={()=>nav("/upload")}>
          Get Started
        </button>
      </div>
    </div>
  );
}

export default Landing;