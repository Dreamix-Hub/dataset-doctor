import {
  Sparkles,
  ArrowRight
} from "lucide-react";


function AIAnalysis({ analysis }) {

  return (
    <section className="ai-section">

      <div className="ai-header">

        <div className="ai-title">

          <div className="ai-icon">
            <Sparkles size={20} />
          </div>

          <div>
            <span>
              Powered by Gemma
            </span>

            <h2>
              AI interpretation
            </h2>
          </div>

        </div>

      </div>


      <div className="ai-summary">
        {analysis.summary}
      </div>


      <div className="ai-findings">

        {analysis.findings.map(
          (finding, index) => (

            <div
              className="ai-finding"
              key={`${finding.type}-${index}`}
            >

              <div className="ai-finding-label">
                {finding.severity}
              </div>

              <h3>
                {finding.title}
              </h3>

              <p>
                {finding.explanation}
              </p>

              <div className="ai-action">
                <ArrowRight size={16} />

                <span>
                  {finding.action}
                </span>
              </div>

            </div>

          )
        )}

      </div>


      {analysis.next_steps.length > 0 && (
        <div className="next-steps">

          <span className="section-eyebrow">
            Recommended next steps
          </span>

          <div className="next-step-list">

            {analysis.next_steps.map(
              (step, index) => (

                <div
                  className="next-step"
                  key={index}
                >

                  <span>
                    {index + 1}
                  </span>

                  <p>
                    {step}
                  </p>

                </div>

              )
            )}

          </div>

        </div>
      )}

    </section>
  );
}


export default AIAnalysis;