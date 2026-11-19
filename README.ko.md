[English](./README.md) · **한국어**

# AI 에이전트 스킬 선택 평가 도구

이 프로젝트는 LLM이 사용자 요청에 맞는 스킬을 선택하는지 평가합니다. 첫 실험에서는 `docx`, `pdf`, `summarize`를 선택 후보로 사용하며, 요청에 맞는 스킬이 없으면 `none`을 선택합니다.

두 스킬이 모두 적용될 수 있을 때는 입력 파일의 형식보다 사용자가 원하는 결과를 우선합니다. 예를 들어 “이 PDF의 핵심 내용을 다섯 가지로 정리해 줘”는 `summarize`로, “이 PDF의 마지막 페이지를 회전해 줘”는 `pdf`로 분류합니다.

## 스킬 구성

| 스킬 | 프로젝트에서의 역할 |
|---|---|
| `docx` | 페이지 번호 추가, `.docx` 파일 편집 등 Word 문서 작업을 위한 선택 후보입니다. |
| `pdf` | 페이지 회전, 파일 병합, 표 추출 등 PDF 작업을 위한 선택 후보입니다. |
| `summarize` | 특정 자료의 핵심 내용을 요약하는 요청을 위한 선택 후보입니다. 이 프로젝트를 위해 작성했습니다. |
| `skill-creator` | 스킬을 선택해야 하는 경우와 선택하지 않아야 하는 경우의 평가 사례를 설계할 때 참고합니다. |

라우터는 각 후보의 `SKILL.md`에 있는 `name`과 `description`을 사용합니다. 요청마다 `docx`, `pdf`, `summarize`, `none` 중 하나를 반환하며, 평가는 스킬 선택 단계까지 진행합니다.

## 평가 예시

| 사용자 요청 | 정답 라벨 |
|---|---|
| “이 Word 문서에 페이지 번호를 넣어 줘.” | `docx` |
| “이 PDF의 마지막 페이지를 회전해 줘.” | `pdf` |
| “이 회의록에서 핵심 내용만 뽑아 줘.” | `summarize` |
| “이 PDF의 핵심 내용을 다섯 가지로 정리해 줘.” | `summarize` |
| “이 Word 문서에서 꼭 알아야 할 내용만 알려 줘.” | `summarize` |
| “보고서 요약문은 어떻게 쓰면 좋을까?” | `none` |

JSONL 데이터셋의 각 줄에는 사용자 요청과 정답 라벨이 들어갑니다.

```jsonl
{"request":"Summarize this PDF in five bullets.","expected_skill":"summarize"}
```

## 평가 절차

1. 각 선택 후보의 `SKILL.md`에서 스킬 이름과 설명을 읽습니다.
2. 모델에 요청을 하나씩 전달하고 스킬 이름 또는 `none`을 반환하도록 합니다.
3. 예측 라벨과 정답 라벨을 비교해 정답 수를 기록하고 오분류 사례를 확인합니다.
4. 개발용 사례를 바탕으로 오류를 분석합니다. 스킬 설명을 수정한 경우, 별도로 보관한 동일한 평가 사례에서 같은 모델과 설정으로 수정 전후의 결과를 비교합니다.

## 진행 상황

스킬 정의와 초기 평가 사례를 준비했습니다. 다음 단계는 기준 평가를 실행하고 사용한 모델, 정답 수, 오분류 사례를 기록하는 것입니다.

## 출처 및 라이선스

`docx`, `pdf`, `skill-creator`는 [Anthropic의 Agent Skills 저장소](https://github.com/anthropics/skills/tree/main/skills)에서 가져왔으며 Apache 2.0 라이선스가 적용됩니다. 각 스킬 폴더의 `LICENSE.txt`에서 라이선스를 확인할 수 있습니다. `summarize`는 이 프로젝트를 위해 작성했습니다.

[`docx` 스킬](./skills/docx/SKILL.md)은
[Anthropic의 Agent Skills 저장소](https://github.com/anthropics/skills/tree/main/skills/docx)의
스킬을 수정해 사용합니다. 모델이 일반적인 템플릿 작성 요청이나 붙여넣은 텍스트의
수정 요청에도 `docx`를 선택하는 사례를 확인했습니다. 이에 기존 Word 문서를
다루거나 결과물을 Word 파일로 명시한 경우에만 선택하도록 스킬 설명을 수정했습니다.
원본 라이선스는 [LICENSE.txt](./skills/docx/LICENSE.txt)에 포함되어 있습니다.
