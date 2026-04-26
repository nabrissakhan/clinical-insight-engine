import sys

# Import pprint so the retrieved facts are easier to read in the terminal.
from pprint import pprint

# Import functions for loading patient data and retrieving facts from the FHIR bundle.
from src.retriever import load_patient_bundle, retrieve_patient_facts

# Import the analyzer function that turns retrieved facts into an insight summary.
from src.analyzer import generate_clinical_insight

# Import the guardrail function that validates the clinical insight before display.
from src.guardrails import validate_clinical_output

# Import the evaluator function that assigns a confidence score based on data availability and insight length.
from src.evaluator import evaluate_confidence

# Define the file path to the sample patient data.
DEFAULT_DATA_PATH = "data/sample_patient.json"

# Only run this block if the script is executed directly.
if __name__ == "__main__":

    data_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATA_PATH

    # Load the full FHIR patient bundle from the JSON file.
    patient_bundle = load_patient_bundle(data_path)

    # Retrieve structured clinical facts from the bundle.
    facts = retrieve_patient_facts(patient_bundle)

    # Generate a clinical insight summary from the retrieved facts.
    insight = generate_clinical_insight(facts)

    # Run the guardrail check on the generated insight.
    guardrail_result = validate_clinical_output(insight)

    # Compute a confidence evaluation based on data availability and insight length.
    evaluation = evaluate_confidence(facts, insight)

    # Print the retrieved facts so we can verify the retrieval step.
    print("\n" + "="*40)
    print("=== Retrieved Patient Facts ===\n")
    pprint(facts)

    # Print the guardrail validation result.
    print("\n" + "="*40)
    print("=== Guardrail Check ===\n")
    pprint(guardrail_result)

    # Print the confidence evaluation.
    print("\n" + "="*40)
    print("=== Evaluation ===\n")
    pprint(evaluation)

    # Only show the insight if it passes validation.
    if guardrail_result.get("passed", False):
        print("\n" + "="*40)
        print("=== Clinical Insight Summary ===\n")
        print(insight)
    else:
        print("\nInsight blocked due to guardrail violations.")
        issues = guardrail_result.get("issues", [])
        if issues:
            print("\nIssues:")
            for issue in issues:
                print(f"- {issue}")