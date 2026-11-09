# Purpose: Assign deterministic evidence confidence and severity labels to a finding record.
# Location: SCRIPTS/08-cybersecurity/finding-confidence/score_finding.py
# Input/output: one JSON finding object to a JSON score; invalid input exits 2.
# Requirements: Python 3.10+, standard library only; no network or exploit evaluation.
# Usage from root: python SCRIPTS/08-cybersecurity/finding-confidence/score_finding.py "{\"evidence\":[{\"kind\":\"response\",\"quality\":\"strong\"}],\"impact\":\"high\"}"
# Limits: at most 20 evidence items; output is a triage aid and never proves exploitability.
"""Score evidence quality for triage without declaring a vulnerability confirmed."""
import argparse
import json

MAX_EVIDENCE = 20
QUALITY_POINTS = {"weak": 1, "moderate": 2, "strong": 3}
IMPACT_LEVELS = {"informational", "low", "medium", "high", "critical"}


def score_finding(finding):
    """Return evidence score, confidence and bounded severity label."""
    if not isinstance(finding, dict):
        raise ValueError("finding must be an object")
    evidence = finding.get("evidence", [])
    impact = finding.get("impact", "informational")
    if not isinstance(evidence, list) or not evidence or len(evidence) > MAX_EVIDENCE:
        raise ValueError(f"evidence must contain 1-{MAX_EVIDENCE} items")
    if impact not in IMPACT_LEVELS:
        raise ValueError("impact must be a known severity label")
    points = 0
    for item in evidence:
        if not isinstance(item, dict) or item.get("quality") not in QUALITY_POINTS:
            raise ValueError("each evidence item needs weak, moderate or strong quality")
        points += QUALITY_POINTS[item["quality"]]
    average = points / len(evidence)
    confidence = "high" if average >= 2.5 and len(evidence) >= 2 else "medium" if average >= 2 else "low"
    return {"evidence_points": points, "evidence_items": len(evidence), "confidence": confidence, "severity": impact, "confirmed": False}


def main():
    # Keep scoring deterministic and explicit so a human can reproduce every label.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("finding_json")
    args = parser.parse_args()
    try:
        print(json.dumps(score_finding(json.loads(args.finding_json)), ensure_ascii=True))
    except (ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
