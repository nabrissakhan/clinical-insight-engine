# Import Python's built-in json module so we can read .json files.
import json


# Define a function that loads a patient JSON file from a file path.
def load_patient_bundle(file_path):
    # Open the JSON file in read mode.
    with open(file_path, "r", encoding="utf-8") as file:
        # Convert the JSON text into a Python dictionary.
        patient_bundle = json.load(file)

    # Return the full patient bundle so other functions can use it.
    return patient_bundle


# Define a helper function to safely get display text from FHIR CodeableConcept-style fields.
def get_code_text(code_object):
    # If the object has a "text" field, use that first because it is human-readable.
    if code_object.get("text"):
        return code_object["text"]

    # Otherwise, look for a coding list.
    coding_list = code_object.get("coding", [])

    # If coding exists and the first coding has a display value, return it.
    first_coding = get_first_item(coding_list)
    if first_coding.get("display"):
        return first_coding["display"]

    # If no useful text is found, return a safe fallback.
    return "Unknown"


# Define a helper function to safely get the first item from a list.
def get_first_item(items):
    # Return the first item in a list if it exists; otherwise return an empty dictionary.
    return items[0] if isinstance(items, list) and len(items) > 0 else {}


# Define the main retrieval function that extracts relevant clinical facts.
def retrieve_patient_facts(patient_bundle):
    # Create a dictionary to store the facts we retrieve from the FHIR bundle.
    facts = {
        "patient": {},
        "conditions": [],
        "medications": [],
        "observations": [],
        "diagnostic_reports": []
    }

    # Loop through each entry in the FHIR Bundle.
    for entry in patient_bundle.get("entry", []):
        # Get the actual FHIR resource inside this entry.
        resource = entry.get("resource", {})

        # Get the resource type, such as Patient, Condition, MedicationRequest, or Observation.
        resource_type = resource.get("resourceType")

        # Handle Patient resources.
        if resource_type == "Patient":
            # Get the first name object safely using get_first_item.
            name = get_first_item(resource.get("name", []))

            # Store basic patient demographic/context information.
            facts["patient"] = {
                "id": resource.get("id", "Unknown"),
                "family_name": name.get("family", "Unknown"),
                "given_names": name.get("given", []),
                "gender": resource.get("gender", "Unknown"),
                "birth_date": resource.get("birthDate", "Unknown")
            }

        # Handle Condition resources.
        elif resource_type == "Condition":
            # Extract the condition name from the FHIR code object.
            condition_name = get_code_text(resource.get("code", {}))

            # Store condition details.
            facts["conditions"].append({
                "condition": condition_name,
                "clinical_status": get_first_item(
                    resource.get("clinicalStatus", {}).get("coding", [])
                ).get("code", "Unknown"),
                "onset": resource.get("onsetDateTime", "Unknown")
            })

        # Handle MedicationRequest resources.
        elif resource_type == "MedicationRequest":
            # Your JSON uses medication.concept, which is modern FHIR-style structure.
            medication_concept = resource.get("medication", {}).get("concept", {})

            # Extract the medication name.
            medication_name = get_code_text(medication_concept)

            # Extract dosage text if available.
            dosage_text = get_first_item(
                resource.get("dosageInstruction", [])
            ).get("text", "No dosage text available")

            # Store medication details.
            facts["medications"].append({
                "medication": medication_name,
                "status": resource.get("status", "Unknown"),
                "intent": resource.get("intent", "Unknown"),
                "dosage": dosage_text
            })

        # Handle Observation resources, such as labs.
        elif resource_type == "Observation":
            # Extract the observation name, such as HbA1c or eGFR.
            observation_name = get_code_text(resource.get("code", {}))

            # Get the valueQuantity object, which usually stores numeric lab values.
            value_quantity = resource.get("valueQuantity", {})

            # Safely extract interpretation using get_first_item at each level.
            interpretation_item = get_first_item(resource.get("interpretation", []))
            interpretation_coding = get_first_item(interpretation_item.get("coding", []))
            interpretation = interpretation_coding.get("display", "Unknown")

            # Store observation details.
            facts["observations"].append({
                "observation": observation_name,
                "value": value_quantity.get("value", "Unknown"),
                "unit": value_quantity.get("unit", ""),
                "date": resource.get("effectiveDateTime", "Unknown"),
                "interpretation": interpretation
            })

        # Handle DiagnosticReport resources.
        elif resource_type == "DiagnosticReport":
            # Extract the diagnostic report name.
            report_name = get_code_text(resource.get("code", {}))

            # Store report summary details.
            facts["diagnostic_reports"].append({
                "report": report_name,
                "date": resource.get("effectiveDateTime", "Unknown"),
                "conclusion": resource.get("conclusion", "No conclusion available")
            })

    # Return the retrieved facts.
    return facts
