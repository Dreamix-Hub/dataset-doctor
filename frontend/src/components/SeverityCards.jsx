import {
  AlertCircle,
  AlertTriangle,
  Info
} from "lucide-react";


function SeverityCards({ analysis }) {

  const cards = [
    {
      label: "Critical",
      value: analysis.critical_count,
      icon: AlertCircle,
      className: "critical",
    },
    {
      label: "Warnings",
      value: analysis.warning_count,
      icon: AlertTriangle,
      className: "warning",
    },
    {
      label: "Info",
      value: analysis.info_count,
      icon: Info,
      className: "info",
    },
  ];


  return (
    <div className="severity-grid">

      {cards.map((card) => {

        const Icon = card.icon;

        return (
          <div
            className={`severity-card ${card.className}`}
            key={card.label}
          >

            <Icon size={20} />

            <div>
              <strong>
                {card.value}
              </strong>

              <span>
                {card.label}
              </span>
            </div>

          </div>
        );
      })}

    </div>
  );
}


export default SeverityCards;