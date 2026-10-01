# 🩺 Dataset Doctor

> **Find problems in your dataset before they find you.**

Dataset Doctor is an open-source AI-powered dataset quality and analysis tool that helps developers and data scientists understand whether a dataset is ready for machine-learning training.

It combines **deterministic Python-based statistical analysis** with **Gemma** to detect potential data-quality problems and explain what they mean and what should be done about them.

The core philosophy is simple:

> **Python calculates the evidence. Gemma explains the evidence.**

---

## ✨ Why Dataset Doctor?

Before training a machine-learning model, data scientists usually spend significant time inspecting and cleaning their datasets.

Common problems include:

* Missing values
* Duplicate records
* Outliers
* Class imbalance
* Highly correlated features
* Suspicious identifier columns
* Constant or low-variance features
* Incorrect data types
* Unusual distributions
* Potential target-variable problems

These problems can negatively affect model training and may lead to misleading results.

Dataset Doctor automates the initial investigation and produces a structured dataset-health report.

---

## 🎯 What Dataset Doctor Does

You upload a CSV dataset and Dataset Doctor:

```text
CSV Dataset
     │
     ▼
┌─────────────────────┐
│ Python Data         │
│ Profiler            │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Deterministic       │
│ Diagnosis Engine    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Dataset Findings    │
│ + Evidence          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Gemma               │
│ Explanation Layer   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Dataset Health      │
│ Report              │
└─────────────────────┘
```

The system separates **analysis** from **interpretation**.

Python performs the actual calculations and determines findings.

Gemma receives those findings and explains them in concise, human-readable language.

This prevents the language model from being responsible for calculating or inventing statistical evidence.

---

# 🚀 Features

## 📊 Dataset Profiling

Dataset Doctor profiles the uploaded dataset and extracts information such as:

* Number of rows
* Number of columns
* Column names
* Data types
* Missing values
* Unique values
* Numerical columns
* Categorical columns
* Basic dataset statistics

---

## 🔍 Automated Dataset Diagnosis

The diagnosis engine currently checks for several common dataset-quality problems.

### Missing Values

Detects columns containing missing values and reports their presence.

### Outliers

Uses the **Interquartile Range (IQR)** method to identify potential numerical outliers.

### Class Imbalance

Checks target-class distributions when a target column is provided.

### High Correlation

Identifies numerical feature pairs with unusually high correlation.

### Suspicious Identifiers

Detects columns that appear to represent record identifiers, such as:

```text
customer_id
user_id
record_id
uuid
```

The detector does not simply assume that every unique numerical column is an identifier.

It combines uniqueness with column-name signals to reduce false positives.

---

## 🤖 Gemma-Powered Explanations

After Python identifies a finding, Gemma explains:

1. What the finding means
2. Why it matters
3. What action should be considered

For example:

```text
Python:
customer_id appears to be a suspicious identifier
because it contains 100% unique values.

Gemma:
This column likely identifies individual records
rather than representing a useful predictive feature.

Action:
Check whether customer_id should be excluded
from model training.
```

Gemma is therefore an **interpretation layer**, not the source of statistical truth.

---

# 🧠 Architecture

Dataset Doctor follows a layered architecture.

```text
                    ┌─────────────────────┐
                    │      React UI       │
                    │   Dataset Upload    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI API     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Dataset Loader    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Dataset Profiler   │
                    │       Python        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Diagnosis Engine    │
                    │       Python        │
                    └──────────┬──────────┘
                               │
                         Findings
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Gemma Service     │
                    │ Explanation Layer   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    API Response     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    React Report     │
                    └─────────────────────┘
```

---

# 🧩 Technology Stack

## Backend

* Python
* FastAPI
* Pandas
* Pydantic
* Google GenAI SDK
* Gemma
* Uvicorn
* uv

## Frontend

* React
* Vite
* JavaScript
* Lucide React
* CSS

## AI

Dataset Doctor currently uses:

```text
Gemma 4 26B A4B IT
```

through the Gemini API.

Gemma is an open-weight model family from Google DeepMind, but its use is governed by Google's applicable Gemma terms rather than the MIT license used for this project's source code.

---

# 📁 Project Structure

```text
dataset-doctor/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── schema.py
│   │
│   ├── profiler/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── schema.py
│   │   ├── profiler.py
│   │   └── checks.py
│   │
│   ├── diagnosis/
│   │   ├── __init__.py
│   │   ├── schema.py
│   │   ├── engine.py
│   │   ├── missing.py
│   │   ├── outliers.py
│   │   ├── imbalance.py
│   │   ├── correlation.py
│   │   └── identifiers.py
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── gemma.py
│   │   ├── prompts.py
│   │   ├── schema.py
│   │   └── service.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
│
├── frontend/
│   ├── public/
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadZone.jsx
│   │   │   ├── DatasetStats.jsx
│   │   │   ├── SeverityCards.jsx
│   │   │   ├── FindingCard.jsx
│   │   │   ├── FindingList.jsx
│   │   │   ├── AIAnalysis.jsx
│   │   │   └── LoadingState.jsx
│   │   │
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── tests/
│   ├── test_profiler.py
│   ├── test_diagnosis.py
│   └── test_ai.py
│
├── sample_data/
│   ├── sample.csv
│   └── classification.csv
│
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
├── LICENSE
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/dataset-doctor.git
cd dataset-doctor
```

Replace `YOUR_USERNAME` with your GitHub username.

---

# 🐍 Backend Setup

Dataset Doctor uses [`uv`](https://docs.astral.sh/uv/) for Python environment and dependency management.

Install the dependencies:

```bash
uv sync
```

If dependencies have not yet been added:

```bash
uv add fastapi uvicorn pandas pydantic google-genai python-multipart
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMMA_MODEL_ID=gemma-4-26b-a4b-it
GEMMA_MAX_OUTPUT_TOKENS=200
GEMMA_TEMPERATURE=0.1
```

Never commit your real API key.

Your `.gitignore` should contain:

```gitignore
.env
__pycache__/
.pytest_cache/
.venv/
node_modules/
dist/
```

You can provide an `.env.example` file:

```env
GEMINI_API_KEY=
GEMMA_MODEL_ID=gemma-4-26b-a4b-it
GEMMA_MAX_OUTPUT_TOKENS=200
GEMMA_TEMPERATURE=0.1
```

---

# ▶️ Running the Backend

From the project root:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

# ⚛️ Frontend Setup

Move into the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# 🔗 Frontend → Backend

The frontend communicates with:

```text
POST /analyze
```

The API accepts:

* CSV file
* Optional target column

Example request:

```text
POST /analyze

file = dataset.csv
target_column = churn
```

The backend then returns:

```text
Dataset profile
+
Python findings
+
Evidence
+
Recommendations
+
Gemma explanations
```

---

# 🧪 Running Tests

Run the complete test suite:

```bash
uv run pytest
```

The tests cover:

* Dataset profiling
* Diagnosis logic
* Missing-value detection
* Outlier detection
* Class imbalance
* Correlation detection
* Identifier detection
* AI service behavior

---

# 📡 API Example

## `POST /analyze`

Example response:

```json
{
  "filename": "classification.csv",
  "rows": 20,
  "columns": 6,
  "target_column": "churn",
  "status": "completed",
  "critical_count": 0,
  "warning_count": 2,
  "info_count": 0,
  "findings": [
    {
      "type": "suspicious_identifier",
      "severity": "warning",
      "title": "Potential identifier column 'customer_id'",
      "message": "Column 'customer_id' appears to behave like an identifier.",
      "column": "customer_id",
      "columns": [],
      "evidence": {
        "unique_ratio": 1.0,
        "unique_percentage": 100.0,
        "name_suggests_identifier": true,
        "numeric": true
      },
      "recommendation": "Check whether this column identifies individual records rather than representing a meaningful predictive feature."
    }
  ],
  "ai_analysis": {
    "summary": "The dataset has detected issues that should be reviewed before machine-learning training.",
    "findings": [],
    "next_steps": []
  }
}
```

---

# 🔬 Design Principle: Evidence First

A major design decision in Dataset Doctor is keeping statistical analysis separate from language generation.

### ❌ Traditional AI approach

```text
Dataset
   ↓
LLM
   ↓
"Here are some problems I found..."
```

This can lead to:

* Hallucinated statistics
* Invented findings
* Incorrect column names
* Inconsistent severity
* Unverifiable conclusions

### ✅ Dataset Doctor approach

```text
Dataset
   ↓
Python
   ↓
Measured evidence
   ↓
Deterministic findings
   ↓
Gemma
   ↓
Human-readable explanation
```

Gemma is explicitly instructed not to:

* Create new findings
* Change severity
* Invent statistics
* Invent columns
* Invent evidence
* Question whether a supplied finding exists

This makes the AI layer more controlled and auditable.

---

# 🩺 Finding Severity

Dataset Doctor uses three severity levels:

| Severity    | Meaning                                                            |
| ----------- | ------------------------------------------------------------------ |
| 🔴 Critical | Potentially serious issue that should be addressed before training |
| 🟡 Warning  | Potential problem that should be reviewed                          |
| 🔵 Info     | Informational observation                                          |

Severity is determined by the deterministic diagnosis engine, not by Gemma.

---

# 📊 Current Detection Capabilities

| Check                     | Python Analysis | Gemma Explanation |
| ------------------------- | --------------: | ----------------: |
| Missing values            |               ✅ |                 ✅ |
| Outliers                  |               ✅ |                 ✅ |
| Class imbalance           |               ✅ |                 ✅ |
| High correlation          |               ✅ |                 ✅ |
| Suspicious identifiers    |               ✅ |                 ✅ |
| Constant columns          |              🔜 |                🔜 |
| Near-zero variance        |              🔜 |                🔜 |
| Duplicate rows            |              🔜 |                🔜 |
| High-cardinality columns  |              🔜 |                🔜 |
| Data-type inconsistencies |              🔜 |                🔜 |
| Target leakage            |              🔜 |                🔜 |
| Distribution analysis     |              🔜 |                🔜 |

---

# 🖥️ User Interface

The frontend provides:

### Dataset Upload

Drag-and-drop CSV upload interface.

### Dataset Overview

Displays:

* Dataset filename
* Number of rows
* Number of columns
* Target column

### Severity Overview

Displays:

* Critical findings
* Warnings
* Informational findings

### Python Findings

Each finding displays:

* Finding type
* Severity
* Title
* Evidence/message
* Affected columns
* Recommended action

### Gemma Interpretation

Gemma provides a human-readable explanation of selected findings.

### Recommended Next Steps

The application summarizes practical actions that can be taken before model training.

---

# 🔒 Privacy

Dataset Doctor is designed around user-provided datasets.

When using the Gemini API for Gemma explanations, dataset-related finding information is sent to the configured Google AI service as part of the API request.

Do **not** upload sensitive, confidential, proprietary, or personally identifiable datasets unless you understand and accept the applicable service terms and privacy requirements.

For production deployments, additional privacy controls should be implemented.

---

# ⚠️ Limitations

Dataset Doctor is an **initial dataset investigation tool**, not a replacement for a complete data-science workflow.

A detected finding does not automatically mean the dataset is unusable.

For example:

* An outlier may be a legitimate observation.
* A highly correlated feature may still be useful depending on the model.
* An identifier may be needed for joining datasets.
* Class imbalance may be expected in the real-world problem.
* Missing values may have meaningful semantics.

The tool provides evidence and recommendations that should be reviewed by the user.

---

# 🛣️ Roadmap

## Phase 1 — Dataset Profiler

* [x] CSV loading
* [x] Dataset dimensions
* [x] Column profiling
* [x] Data types
* [x] Missing-value statistics

## Phase 2 — Deterministic Diagnosis

* [x] Missing values
* [x] Outlier detection
* [x] Class imbalance
* [x] Correlation analysis
* [x] Suspicious identifier detection
* [ ] Duplicate detection improvements
* [ ] Near-zero variance
* [ ] High-cardinality detection
* [ ] Data-type consistency checks

## Phase 3 — Gemma Integration

* [x] Gemini API integration
* [x] Gemma model integration
* [x] Structured JSON responses
* [x] Finding-level explanations
* [x] Controlled prompts
* [x] Evidence-first architecture

## Phase 4 — API

* [x] FastAPI service
* [x] `/analyze`
* [x] Structured response models
* [x] CORS configuration

## Phase 5 — Frontend

* [x] React + Vite
* [x] CSV upload
* [x] Dataset analysis
* [x] Loading state
* [x] Dataset statistics
* [x] Severity overview
* [x] Finding cards
* [x] Gemma analysis
* [x] Recommended next steps

## Future

* [ ] Dataset preview
* [ ] Interactive visualizations
* [ ] Correlation heatmap
* [ ] Distribution charts
* [ ] Target-column dropdown
* [ ] More leakage detection
* [ ] Duplicate analysis
* [ ] Automatic cleaning suggestions
* [ ] Dataset comparison
* [ ] Exportable reports
* [ ] Docker deployment
* [ ] Production deployment
* [ ] Support for additional dataset formats

---

# 🤝 Contributing

Contributions are welcome.

## 1. Fork the repository

Create your own fork on GitHub.

## 2. Create a branch

```bash
git checkout -b feature/your-feature
```

## 3. Make your changes

Follow the existing project structure and keep analysis logic deterministic where possible.

## 4. Run tests

```bash
uv run pytest
```

## 5. Commit your changes

```bash
git add .
git commit -m "Add your feature"
```

## 6. Push your branch

```bash
git push origin feature/your-feature
```

## 7. Open a Pull Request

Explain:

* What you changed
* Why you changed it
* How you tested it

---

# 🧑‍💻 Development Philosophy

Dataset Doctor follows several principles:

### 1. Evidence before explanation

Statistics should come from deterministic code.

### 2. AI should explain, not fabricate

Gemma should interpret existing evidence rather than inventing dataset findings.

### 3. Structured outputs

Important information is represented using Pydantic models rather than uncontrolled text.

### 4. Small, testable components

Dataset checks are separated into individual modules.

### 5. Human remains in the loop

Dataset Doctor assists the data scientist; it does not automatically decide how the dataset must be changed.

---

# 🌟 Why Gemma?

Gemma is an open-weight model family developed by Google DeepMind. It is intended as a foundation that developers and researchers can use to build customized AI applications.

Dataset Doctor uses Gemma specifically for the **interpretation layer**.

Instead of asking an LLM to analyze raw data directly:

```text
Raw Dataset → LLM → Analysis
```

Dataset Doctor uses:

```text
Raw Dataset
     ↓
Python Statistical Analysis
     ↓
Structured Findings
     ↓
Gemma
     ↓
Natural-Language Explanation
```

This allows the project to demonstrate a practical role for an open-weight AI model while keeping statistical evidence grounded in deterministic computation.

---

# 📜 License

## Dataset Doctor

The Dataset Doctor source code is released under the **MIT License**.

The MIT License permits users to use, copy, modify, merge, publish, distribute, sublicense, and sell copies of the software, subject to the license conditions.

Create a file named:

```text
LICENSE
```

and place the MIT License in it.

Use the following copyright notice:

```text
MIT License

Copyright (c) 2026 Muhammad Abdullah

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

The SPDX identifier for the license is:

```text
MIT
```

You can also identify the project license using:

```text
SPDX-License-Identifier: MIT
```

SPDX maintains the standardized identifier and canonical license information.

---

# 🤖 Gemma License / Terms Notice

**Important:** The MIT License applies to the Dataset Doctor source code that you own. It does **not** replace or override the terms applicable to Gemma.

Dataset Doctor uses Gemma through Google's AI services. Gemma is governed by Google's applicable **Gemma Terms of Use**. Developers distributing Gemma or Model Derivatives may have additional notice and terms obligations under those terms.

For the current Gemma terms, refer to Google's official documentation:

[Gemma Terms of Use](https://ai.google.dev/gemma/terms?utm_source=chatgpt.com)

---

# 📚 Third-Party Technologies

Dataset Doctor is built using open-source and third-party technologies.

| Technology       | Purpose                               |
| ---------------- | ------------------------------------- |
| Python           | Backend language                      |
| FastAPI          | API framework                         |
| Pandas           | Dataset analysis                      |
| Pydantic         | Data validation                       |
| Uvicorn          | ASGI server                           |
| Google GenAI SDK | Gemini API communication              |
| Gemma            | AI explanation model                  |
| React            | Frontend                              |
| Vite             | Frontend build tool                   |
| Lucide React     | UI icons                              |
| uv               | Python package/environment management |

Each third-party dependency remains subject to its own applicable license and terms.

---

# 🧪 Example Workflow

Suppose a dataset contains:

```text
customer_id
age
income
credit_score
visits
churn
```

Dataset Doctor can identify:

```text
customer_id
    ↓
Potential identifier
    ↓
100% unique
```

Python generates the evidence:

```json
{
  "unique_ratio": 1.0,
  "unique_percentage": 100.0,
  "name_suggests_identifier": true
}
```

Gemma then explains the finding:

```text
This column likely identifies individual records
rather than representing a useful predictive feature.
```

The user can then decide whether the column should be removed, retained, or used for another purpose.

---

# 🎓 Project Goal

Dataset Doctor was created to explore how **open-weight AI models can work alongside deterministic data-science tooling** to make dataset investigation more accessible.

The project demonstrates that an AI model does not have to perform every part of a workflow.

Instead:

> **Let code measure the data. Let AI explain the measurements. Let humans make the final decisions.**

---

# 👨‍💻 Author

**Muhammad Abdullah**

AI / ML Developer
Backend Developer

---

# ⭐ Support the Project

If Dataset Doctor is useful to you:

* ⭐ Star the repository
* 🐛 Report issues
* 💡 Suggest improvements
* 🔀 Submit pull requests
* 📢 Share the project

---

## 📄 License Summary

```text
Dataset Doctor source code
        ↓
MIT License

Gemma
        ↓
Google Gemma Terms of Use

Third-party dependencies
        ↓
Their respective licenses
```

**SPDX-License-Identifier: MIT**
