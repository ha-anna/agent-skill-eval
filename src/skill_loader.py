from pathlib import Path

import yaml


def load_skill(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()

    end = lines.index("---", 1)

    frontmatter = "\n".join(lines[1:end])
    metadata = yaml.safe_load(frontmatter)

    return {
        "name": metadata["name"],
        "description": metadata["description"],
    }


if __name__ == "__main__":
    for skill_name in ("summarize", "pdf", "docx"):
        path = Path("skills") / skill_name / "SKILL.md"
        skill = load_skill(path)

        print(skill["name"])
        print(skill["description"])
        print()
