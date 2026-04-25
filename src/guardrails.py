# Define a constant for minimum output length so the intent is clear and easy to adjust later.
MIN_OUTPUT_LENGTH = 100


# Define a function that checks whether the generated clinical insight is safe to show.
def validate_clinical_output(insight_text):
    # Create an empty list to store any issues found during validation.
    issues = []

    # Convert the insight text to lowercase so checks are case-insensitive.
    lower_text = insight_text.lower()

    # Define phrases that would be unsafe because they sound like medical advice.
    unsafe_phrases = [
        # Second-person (direct advice)
        "you should take",
        "you should stop",
        "you should start",
        "increase your dose",
        "decrease your dose",
        "this confirms",
        "you have been diagnosed",

        # Third-person / clinical phrasing (important for your analyzer output style)
        "recommend increasing",
        "recommend decreasing",
        "should be prescribed",
        "requires immediate",
        "must take"
    ]

    # Loop through each unsafe phrase.
    for phrase in unsafe_phrases:
        # If the phrase appears in the output, record it as an issue.
        if phrase in lower_text:
            issues.append(f"Unsafe medical advice phrase detected: '{phrase}'")

    # Check that the output includes the educational/synthetic-data disclaimer.
    if "not medical advice" not in lower_text:
        issues.append("Missing safety disclaimer: output should state that it is not medical advice.")

    # Check that the output mentions synthetic data.
    if "synthetic" not in lower_text:
        issues.append("Missing synthetic data disclosure.")

    # Check that the output is not empty or too short to be meaningful.
    if len(insight_text.strip()) < MIN_OUTPUT_LENGTH:
        issues.append(f"Output is too short (minimum {MIN_OUTPUT_LENGTH} characters required).")

    # The output passes guardrails only if no issues were found.
    passed = len(issues) == 0

    # Return a structured validation result.
    return {
        "passed": passed,
        "issues": issues
    }