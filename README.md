# Dataset Doctor

Dataset Doctor is an open-source AI-powered dataset analysis and data-quality tool.

It investigates datasets before machine-learning training and explains potential problems in simple language.

## Tech Stack

- Python
- uv
- Pandas
- NumPy
- SciPy
- Scikit-learn
- FastAPI
- Gemma (future phase)

## Phase 1

Phase 1 focuses on building the dataset profiling engine.

Currently detects:

- Dataset dimensions
- Numerical columns
- Categorical columns
- Datetime columns
- Missing values
- Duplicate rows
- Unique values
- Constant columns
- High-cardinality columns
- Basic numerical statistics

## Requirements

- Python 3.11+
- uv

## Setup

Clone the repository and enter the project:

```bash
cd dataset-doctor