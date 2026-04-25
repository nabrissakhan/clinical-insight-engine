import sys
from pathlib import Path

# Adding the project root to the system path so we can import from src
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Basic test to ensure retrieval works without errors
from src.retriever import load_patient_bundle, retrieve_patient_facts

def test_retrieval_runs():
    data_path = Path("data/sample_patient.json")
    bundle = load_patient_bundle(data_path)
    facts = retrieve_patient_facts(bundle)

    # Check that key sections exist
    assert "patient" in facts
    assert "conditions" in facts
    assert "medications" in facts

    # Check that data was actually extracted
    assert len(facts["conditions"]) > 0
    assert len(facts["medications"]) > 0