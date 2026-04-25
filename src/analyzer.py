# Define a function that turns retrieved patient facts into a readable clinical insight summary.
def generate_clinical_insight(facts):
    # Get patient details from the retrieved facts dictionary.
    patient = facts.get("patient", {})

    # Get lists of conditions, medications, observations, and diagnostic reports.
    conditions = facts.get("conditions", [])
    medications = facts.get("medications", [])
    observations = facts.get("observations", [])
    diagnostic_reports = facts.get("diagnostic_reports", [])

    # Build a readable patient name from given names + family name.
    given_names = " ".join(patient.get("given_names", []))
    family_name = patient.get("family_name", "Unknown")
    patient_name = f"{given_names} {family_name}".strip()

    # Convert condition dictionaries into readable condition names.
    condition_names = [item.get("condition", "Unknown") for item in conditions]

    # Convert medication dictionaries into readable medication names.
    medication_names = [item.get("medication", "Unknown") for item in medications]

    # Create an empty list to store insight bullets.
    insights = []

    # Add a patient context sentence.
    insights.append(
        f"Patient Context: {patient_name} is a synthetic patient with documented clinical history."
    )

    # Add a condition summary if conditions are available.
    if condition_names:
        insights.append(
            "Key Conditions: " + ", ".join(condition_names) + "."
        )

    # Add a medication summary if medications are available.
    if medication_names:
        insights.append(
            "Current Medications: " + ", ".join(medication_names) + "."
        )

    # Look through observations and create lab-specific insight statements.
    for observation in observations:
        # Get the lab name, value, unit, and interpretation.
        lab_name = observation.get("observation", "Unknown lab")
        value = observation.get("value", "Unknown")
        unit = observation.get("unit", "")
        interpretation = observation.get("interpretation", "Unknown")

        # Format value + unit with special handling for percentage values.
        if unit == "%":
            value_str = f"{value}%"
        elif unit:
            value_str = f"{value} {unit}"
        else:
            value_str = str(value)

        # Add a readable lab finding.
        insights.append(
            f"Lab Finding: {lab_name} is {value_str}, flagged as {interpretation}."
        )

    # Add diagnostic report conclusions if available.
    for report in diagnostic_reports:
        # Get the report name and conclusion.
        report_name = report.get("report", "Diagnostic Report")
        conclusion = report.get("conclusion", "No conclusion available")

        # Add a report-based insight.
        insights.append(
            f"{report_name} Conclusion: {conclusion}"
        )

    # Add a responsible AI disclaimer so the output is not framed as medical advice.
    insights.append(
        "Safety Note: This summary is generated from synthetic data for educational purposes and is not medical advice."
    )

    # Join all insight bullets into one formatted output string.
    return "\n".join(f"- {insight}" for insight in insights)