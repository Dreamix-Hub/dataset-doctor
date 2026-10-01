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
- Gemma

## Phase 1 — Dataset Profiler

Phase 1 builds the core dataset profiling engine.

It currently analyzes:

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