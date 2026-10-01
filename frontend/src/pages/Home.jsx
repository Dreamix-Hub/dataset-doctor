import { useState } from "react";

import UploadZone from "../components/UploadZone";
import LoadingState from "../components/LoadingState";
import DatasetStats from "../components/DatasetStats";
import SeverityCards from "../components/SeverityCards";
import FindingList from "../components/FindingList";
import AIAnalysis from "../components/AIAnalysis";

import { analyzeDataset } from "../services/api";


function Home() {
  const [file, setFile] = useState(null);
  const [targetColumn, setTargetColumn] =
    useState("");

  const [analysis, setAnalysis] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  const handleAnalyze = async () => {
    if (!file) {
      return;
    }

    setLoading(true);
    setError("");
    setAnalysis(null);

    try {
      const result =
        await analyzeDataset(
          file,
          targetColumn
        );

      setAnalysis(result);

    } catch (err) {
      setError(
        err.message ||
          "Something went wrong."
      );

    } finally {
      setLoading(false);
    }
  };


  const handleReset = () => {
    setFile(null);
    setTargetColumn("");
    setAnalysis(null);
    setError("");
  };


  if (loading) {
    return (
      <main className="app-shell">
        <LoadingState
          filename={file?.name}
        />
      </main>
    );
  }


  if (analysis) {
    return (
      <main className="app-shell">
        <section className="results-page">

          <div className="results-header">

            <div>
              <div className="badge">
                Analysis Complete
              </div>

              <h1>
                Dataset health report
              </h1>

              <p>
                {analysis.filename}
              </p>
            </div>

            <button
              className="secondary-button"
              onClick={handleReset}
            >
              Analyze another dataset
            </button>

          </div>


          <DatasetStats
            analysis={analysis}
          />


          <SeverityCards
            analysis={analysis}
          />


          <FindingList
            findings={analysis.findings}
          />


          <AIAnalysis
            analysis={analysis.ai_analysis}
          />

        </section>
      </main>
    );
  }


  return (
    <main className="app-shell">

      <section className="hero">

        <div className="badge">
          AI-Powered Dataset Analysis
        </div>

        <h1>
          Find problems in your dataset
          <span>
            before they find you.
          </span>
        </h1>

        <p className="hero-description">
          Dataset Doctor analyzes your dataset,
          detects potential quality issues, and
          uses AI to explain what you should fix
          before machine-learning training.
        </p>


        <UploadZone
          file={file}
          onFileSelect={(selectedFile) => {
            setFile(selectedFile);
            setAnalysis(null);
            setError("");
          }}
        />


        {file && (
          <div className="analysis-controls">

            <div className="selected-file">
              <strong>
                {file.name}
              </strong>

              <span>
                {(file.size / 1024).toFixed(1)} KB
              </span>
            </div>


            <div className="target-control">

              <label htmlFor="target">
                Target column
                <span>
                  optional
                </span>
              </label>

              <input
                id="target"
                type="text"
                placeholder="e.g. churn"
                value={targetColumn}
                onChange={(event) =>
                  setTargetColumn(
                    event.target.value
                  )
                }
              />

            </div>


            <button
              className="primary-button"
              onClick={handleAnalyze}
            >
              Analyze Dataset
            </button>

          </div>
        )}


        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

      </section>

    </main>
  );
}


export default Home;