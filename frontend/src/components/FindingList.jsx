import FindingCard from "./FindingCard";


function FindingList({ findings }) {

  return (
    <section className="findings-section">

      <div className="section-heading">

        <div>
          <span className="section-eyebrow">
            Python analysis
          </span>

          <h2>
            Detected findings
          </h2>
        </div>

        <span className="finding-count">
          {findings.length} findings
        </span>

      </div>


      {findings.length === 0 ? (
        <div className="empty-state">
          <h3>
            No issues detected
          </h3>

          <p>
            Dataset Doctor did not detect any
            configured quality issues.
          </p>
        </div>
      ) : (
        <div className="findings-list">

          {findings.map(
            (finding, index) => (
              <FindingCard
                key={`${finding.type}-${index}`}
                finding={finding}
              />
            )
          )}

        </div>
      )}

    </section>
  );
}


export default FindingList;