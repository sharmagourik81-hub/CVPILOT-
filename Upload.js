import { useNavigate } from "react-router-dom";
import { useState } from "react";

function Upload() {
  const nav = useNavigate();
  const [file, setFile] = useState(null);

  return (
    <div className="page">
      <div className="card">

        <h2>Upload Resume</h2>

        <input type="file" onChange={(e)=>setFile(e.target.files[0])}/>

        {file && <p style={{marginTop:"10px"}}>{file.name}</p>}

        <button onClick={()=>nav("/analyze",{state:{file}})}>
          Next →
        </button>

      </div>
    </div>
  );
}

export default Upload;