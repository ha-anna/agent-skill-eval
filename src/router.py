import json
from pathlib import Path
from urllib.request import Request, urlopen

from src.skill_loader import load_skill


def build_routing_prompt(request, skills):
    skill_options = "\n".join(
        f"- {skill['name']}: {skill['description']}" for skill in skills
    )

    return f"""Choose the skill that best matches the user's request.
        Return exactly one skill name, or none if no skill fits.
        If two skills apply, prioritize the requested outcome over the input format.

        Available skills:
        {skill_options}

        User request:
        {request}
        """


def route_request(user_request, skills):
    prompt = build_routing_prompt(user_request, skills)
    payload = {
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False,
    }

    request = Request(
        "http://ollama:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=120) as response:
        result = json.load(response)

    return result["response"]


if __name__ == "__main__":
    skills = []
    for skill_name in ("summarize", "pdf", "docx"):
        path = Path("skills") / skill_name / "SKILL.md"
        skill = load_skill(path)
        skills.append(skill)

    print(route_request("Give me the gist of these notes.", skills))
    print(route_request("Rotate the last page of this PDF.", skills))
    print(route_request("How do I write a good summary?", skills))
