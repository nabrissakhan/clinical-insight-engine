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


## Pipeline Architecture

```text
load_patient_bundle()
    ↓
retrieve_patient_facts()
    ↓
generate_clinical_insight()
    ↓
validate_clinical_output()   ← checks safety and compliance
    ↓
evaluate_confidence()        ← scores reliability based on data completeness
    ↓
(validation passed?)
  yes → display clinical insight
  no  → display guardrail violations
```

---

## Example Output

```text
========================================
=== Retrieved Patient Facts ===

{'conditions': [{'clinical_status': 'active',
                 'condition': 'Type 2 Diabetes Mellitus',
                 'onset': '2018-06-01'},
                {'clinical_status': 'active',
                 'condition': 'Chronic Kidney Disease Stage 2',
                 'onset': '2021-11-10'}],
 'medications': [{'medication': 'Metformin 500mg'},
                 {'medication': 'Empagliflozin 10mg'}],
 'observations': [{'observation': 'HbA1c', 'value': 7.8, 'interpretation': 'High'},
                  {'observation': 'eGFR (CKD-EPI)', 'value': 68, 'interpretation': 'Low'}]}

========================================
=== Guardrail Check ===

{'passed': True, 'issues': []}

========================================
=== Evaluation ===

{'confidence_score': 1.0, 'confidence_label': 'High confidence'}

========================================
=== Clinical Insight Summary ===

- Patient Context: Elena M Rivera is a synthetic patient with documented clinical history.
- Key Conditions: Type 2 Diabetes Mellitus, Chronic Kidney Disease Stage 2.
- Current Medications: Metformin 500mg, Empagliflozin 10mg.
- Lab Finding: HbA1c is 7.8%, flagged as High.
- Lab Finding: eGFR (CKD-EPI) is 68 mL/min/1.73m2, flagged as Low.
```