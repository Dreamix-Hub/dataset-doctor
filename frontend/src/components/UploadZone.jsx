import { useRef, useState } from "react";
import { Upload, FileSpreadsheet } from "lucide-react";

function UploadZone({ file, onFileSelect }) {
  const inputRef = useRef(null);
  const [dragging, setDragging] = useState(false);

  const handleFile = (selectedFile) => {
    if (!selectedFile) {
      return;
    }

    if (!selectedFile.name.toLowerCase().endsWith(".csv")) {
      alert("Please upload a CSV file.");
      return;
    }

    onFileSelect(selectedFile);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragging(false);

    const droppedFile =
      event.dataTransfer.files[0];

    handleFile(droppedFile);
  };

  return (
    <div
      className={`upload-zone ${
        dragging ? "dragging" : ""
      }`}
      onDragOver={(event) => {
        event.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => {
        setDragging(false);
      }}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".csv"
        hidden
        onChange={(event) =>
          handleFile(event.target.files[0])
        }
      />

      <div className="upload-icon">
        {file ? (
          <FileSpreadsheet size={28} />
        ) : (
          <Upload size={28} />
        )}
      </div>

      <h3>
        {file
          ? "Dataset selected"
          : "Drop your CSV here"}
      </h3>

      <p>
        {file
          ? "Click to choose another file"
          : "or click to browse from your computer"}
      </p>

      <span className="upload-hint">
        CSV files only
      </span>
    </div>
  );
}

export default UploadZone;