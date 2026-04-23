function ProgressBar({ step }) {
  return (
    <div className="progress">
      {[1,2,3,4].map((s) => (
        <div key={s} className={`dot ${step >= s ? "active" : ""}`}>
          {s}
        </div>
      ))}
    </div>
  );
}

export default ProgressBar;