# Minimum length for a meaningful insight output.
MIN_INSIGHT_LENGTH = 100

# Weight assigned to each data component when calculating confidence.
COMPONENT_WEIGHT = 0.2


def evaluate_confidence(facts, insight_text):
    """Compute a simple confidence score based on data availability and output length."""
    # Start with a base score and add COMPONENT_WEIGHT for each data component present.
    score = 0.0
    if facts.get("patient"):
        score += COMPONENT_WEIGHT
    if facts.get("conditions"):
        score += COMPONENT_WEIGHT
    if facts.get("medications"):
        score += COMPONENT_WEIGHT
    if facts.get("observations"):
        score += COMPONENT_WEIGHT
    if facts.get("diagnostic_reports"):
        score += COMPONENT_WEIGHT
    # Reduce confidence if the insight is too short.
    if len(insight_text.strip()) < MIN_INSIGHT_LENGTH:
        score -= 0.1
    # Clamp score to [0.0, 1.0].
    score = max(0.0, min(score, 1.0))
    # Assign a qualitative label based on the numeric score.
    if score >= 0.8:
        label = "High confidence"
    elif score >= 0.5:
        label = "Moderate confidence"
    else:
        label = "Low confidence"
    # Return structured evaluation output.
    return {
        "confidence_score": round(score, 2),
        "confidence_label": label
    }