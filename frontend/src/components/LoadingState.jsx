import { LoaderCircle, Sparkles } from "lucide-react";


function LoadingState({ filename }) {
  return (
    <section className="loading-page">

      <div className="loading-icon">
        <LoaderCircle size={30} />
      </div>

      <div className="badge">
        <Sparkles size={14} />
        Dataset Doctor
      </div>

      <h1>
        Examining your dataset
      </h1>

      <p>
        Python is checking the dataset and
        Gemma is preparing explanations.
      </p>

      {filename && (
        <div className="loading-file">
          {filename}
        </div>
      )}

      <div className="loading-steps">

        <div className="loading-step active">
          <span />
          Profiling dataset
        </div>

        <div className="loading-step active">
          <span />
          Detecting potential issues
        </div>

        <div className="loading-step active">
          <span />
          Generating AI explanations
        </div>

      </div>

    </section>
  );
}


export default LoadingState;