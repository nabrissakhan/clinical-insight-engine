# Import pprint so the retrieved facts are easier to read in the terminal.
from pprint import pprint

# Import both retrieval functions from retriever.
from retriever import load_patient_bundle, retrieve_patient_facts

# Import the analyzer function that turns retrieved facts into an insight summary.
from analyzer import generate_clinical_insight


# Define the file path to the sample patient data.
DATA_PATH = "data/sample_patient.json"


# Only run this block if the script is executed directly.
if __name__ == "__main__":
    # Load the full FHIR patient bundle from the JSON file.
    patient_bundle = load_patient_bundle(DATA_PATH)

    # Retrieve structured clinical facts from the bundle.
    facts = retrieve_patient_facts(patient_bundle)

    # Generate a clinical insight summary from the retrieved facts.
    insight = generate_clinical_insight(facts)

    # Print the retrieved facts so we can verify the retrieval step.
    print("\n=== Retrieved Patient Facts ===\n")
    pprint(facts)

    # Print the generated insight summary.
    print("\n=== Clinical Insight Summary ===\n")
    print(insight)