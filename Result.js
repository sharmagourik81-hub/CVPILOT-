import { useLocation } from "react-router-dom";

function Result() {
  const { state } = useLocation();

  return (
    <div className="page">
      <div className="card">

        <h2>Results</h2>

        <div className="result-grid">

          <div className="box">
            <h3>ATS Score</h3>
            <p>{state.ats_score}</p>
          </div>

          <div className="box">
            <h3>Job Match</h3>
            <p>{state.job_match_score}%</p>
          </div>

          <div className="box">
            <h3>Skills</h3>
            {state.skills_found.map((s,i)=><p key={i}>{s}</p>)}
          </div>

          <div className="box">
            <h3>Missing</h3>
            {state.missing_skills.map((s,i)=><p key={i}>{s}</p>)}
          </div>

        </div>

      </div>
    </div>
  );
}

export default Result;