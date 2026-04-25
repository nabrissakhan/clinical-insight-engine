# Clinical Insight Pipeline: Applied AI System for FHIR Patient Data

A modular Python pipeline that processes a synthetic FHIR R4 patient bundle to extract structured clinical facts, generate a human-readable clinical insight summary, validate it using safety guardrails, and assign a confidence score based on data completeness.

Built as a final project to demonstrate responsible AI system design patterns applied to healthcare data.

---

## Project Structure

```text
clinical-insight-engine/
├── data/
│   └── sample_patient.json   # Synthetic FHIR-style patient bundle
├── src/
│   ├── retriever.py          # Extracts structured clinical facts from FHIR JSON
│   ├── analyzer.py           # Generates a clinical insight summary
│   ├── guardrails.py         # Validates output for safety before display
│   ├── evaluator.py          # Scores confidence based on data availability and output quality
│   └── main.py               # Runs the full end-to-end pipeline
├── tests/
├── assets/
├── README.md
├── model_card.md
└── requirements.txt
```

Each module has a single responsibility, making the pipeline easy to understand, test, and extend.