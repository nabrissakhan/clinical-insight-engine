# Import pprint so the output is easier to read in the terminal.
from pprint import pprint

# Import both functions from retriever in one line (more Pythonic).
from retriever import load_patient_bundle, retrieve_patient_facts


# Define the file path to the sample patient data.
DATA_PATH = "data/sample_patient.json"


# Only run this block if the script is executed directly (not imported).
if __name__ == "__main__":
    # Load the full FHIR patient bundle from the JSON file.
    patient_bundle = load_patient_bundle(DATA_PATH)

    # Retrieve structured clinical facts from the bundle.
    facts = retrieve_patient_facts(patient_bundle)

    # Print a readable label before showing the output.
    print("\n=== Retrieved Patient Facts ===\n")

    # Pretty-print the extracted facts so we can inspect the result.
    pprint(facts)