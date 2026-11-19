import json
from pathlib import Path

from src.router import route_request
from src.skill_loader import load_skill


def grade_prediction(raw_reply, expected):
    try:
        reply = json.loads(raw_reply)
    except json.JSONDecodeError:
        return "invalid_output"

    if not isinstance(reply, dict) or set(reply) != {"label"}:
        return "invalid_output"

    prediction = reply["label"]

    if not isinstance(prediction, str):
        return "invalid_output"

    allowed_labels = {"summarize", "pdf", "docx", "none"}

    if prediction not in allowed_labels:
        return "invalid_output"

    if prediction == expected:
        return "correct"

    if expected == "none":
        return "false_positive"

    return "wrong_label"


if __name__ == "__main__":
    skills = []
    for skill_name in ("summarize", "pdf", "docx"):
        path = Path("skills") / skill_name / "SKILL.md"
        skills.append(load_skill(path))

    correct = 0
    total = 0

    with Path("datasets/routing_dev.jsonl").open(encoding="utf-8") as dataset:
        for line in dataset:
            if not line.strip():
                continue

            case = json.loads(line)
            raw_reply = route_request(case["request"], skills)
            expected = case["expected_skill"]
            status = grade_prediction(raw_reply, expected)

            total += 1
            if status == "correct":
                correct += 1
            else:
                print(f"{status} | request={case['request']!r}")
                print(f"  expected={expected!r} | raw_reply={raw_reply!r}")

    print(f"Correct: {correct}/{total}")
