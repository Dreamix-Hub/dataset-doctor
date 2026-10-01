import {
  AlertTriangle,
  AlertCircle,
  Info,
  ArrowUpRight
} from "lucide-react";


function FindingCard({ finding }) {

  const icons = {
    critical: AlertCircle,
    warning: AlertTriangle,
    info: Info,
  };

  const Icon =
    icons[finding.severity] || Info;


  return (
    <article className="finding-card">

      <div className="finding-top">

        <div
          className={`finding-severity ${finding.severity}`}
        >
          <Icon size={16} />
          {finding.severity}
        </div>

        <span className="finding-type">
          {finding.type.replaceAll("_", " ")}
        </span>

      </div>


      <h3>
        {finding.title}
      </h3>


      <p className="finding-message">
        {finding.message}
      </p>


      {finding.columns?.length > 0 && (
        <div className="column-tags">

          {finding.columns.map(
            (column) => (
              <span key={column}>
                {column}
              </span>
            )
          )}

        </div>
      )}


      {finding.column && (
        <div className="column-tags">
          <span>
            {finding.column}
          </span>
        </div>
      )}


      <div className="recommendation">

        <div>
          <strong>
            Recommended action
          </strong>

          <p>
            {finding.recommendation}
          </p>
        </div>

        <ArrowUpRight size={18} />

      </div>

    </article>
  );
}


export default FindingCard;