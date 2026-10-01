import {
  Database,
  Rows3,
  Columns3,
  Target
} from "lucide-react";


function DatasetStats({ analysis }) {

  const stats = [
    {
      label: "Rows",
      value: analysis.rows,
      icon: Rows3,
    },
    {
      label: "Columns",
      value: analysis.columns,
      icon: Columns3,
    },
    {
      label: "Target",
      value:
        analysis.target_column ||
        "Not specified",
      icon: Target,
    },
  ];


  return (
    <div className="stats-grid">

      <div className="stat-card dataset-name">

        <div className="stat-icon">
          <Database size={20} />
        </div>

        <div>
          <span>Dataset</span>
          <strong>
            {analysis.filename}
          </strong>
        </div>

      </div>


      {stats.map((stat) => {

        const Icon = stat.icon;

        return (
          <div
            className="stat-card"
            key={stat.label}
          >

            <div className="stat-icon">
              <Icon size={20} />
            </div>

            <div>
              <span>{stat.label}</span>
              <strong>{stat.value}</strong>
            </div>

          </div>
        );
      })}

    </div>
  );
}


export default DatasetStats;