const API_BASE_URL = "http://127.0.0.1:8000";

export async function analyzeDataset(
  file,
  targetColumn
) {
  const formData = new FormData();

  formData.append("file", file);

  if (targetColumn) {
    formData.append(
      "target_column",
      targetColumn
    );
  }

  const response = await fetch(
    `${API_BASE_URL}/analyze`,
    {
      method: "POST",
      body: formData,
    }
  );

  let data;

  try {
    data = await response.json();
  } catch {
    throw new Error(
      "The server returned an invalid response."
    );
  }

  if (!response.ok) {
    throw new Error(
      data.detail ||
        "Dataset analysis failed."
    );
  }

  return data;
}