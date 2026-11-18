**English** · [한국어](./README.ko.md)

# Agent Skill Routing Evaluator

This project evaluates whether an LLM selects the appropriate skill for a user request. The first experiment tests routing among `docx`, `pdf`, and `summarize`, with `none` available when no skill fits.

When two skills could apply, the user’s requested outcome takes priority over the source format. For example, “Summarize this PDF in five bullets” should route to `summarize`, while “Rotate the last page of this PDF” should route to `pdf`.

## Skills

| Skill | Role in the project |
|---|---|
| `docx` | Routing candidate for Word document operations, such as adding page numbers or editing a `.docx` file. |
| `pdf` | Routing candidate for PDF operations, such as rotating pages, merging files, or extracting tables. |
| `summarize` | Routing candidate for requests to condense a specific source into its main points. Written for this project. |
| `skill-creator` | Reference for designing test cases that should or should not trigger a skill. |

The router uses the `name` and `description` fields from each candidate’s `SKILL.md`. Each request gets a single label: `docx`, `pdf`, `summarize`, or `none`. The evaluation ends at skill selection.

## Example cases

| User request | Expected label |
|---|---|
| “Add page numbers to this Word document.” | `docx` |
| “Rotate the last page of this PDF.” | `pdf` |
| “Give me the highlights from these meeting notes.” | `summarize` |
| “Summarize this PDF in five bullets.” | `summarize` |
| “Give me the main takeaways from this Word document.” | `summarize` |
| “How do I write a good executive summary?” | `none` |

Each line in the JSONL dataset contains a request and its expected label.

```jsonl
{"request":"Summarize this PDF in five bullets.","expected_skill":"summarize"}
```

## Evaluation plan

1. Load the name and description of each routing candidate from its `SKILL.md`.
2. Send one request at a time to the model and ask it to return a skill name or `none`.
3. Compare each prediction with the expected label. Record the number of correct predictions and inspect the mismatches.
4. Use the development cases to diagnose errors. If a skill description changes, compare the original and revised versions on the same held-out cases using the same model and settings.

## Project status

The skill definitions and initial evaluation cases are ready. The next milestone is a baseline run that records the model used, the number of correct predictions, and the individual mismatches.

## Attribution

`docx`, `pdf`, and `skill-creator` come from [Anthropic’s Agent Skills repository](https://github.com/anthropics/skills/tree/main/skills) and are licensed under Apache 2.0. See the `LICENSE.txt` files in the respective skill folders. The `summarize` skill was written for this project.