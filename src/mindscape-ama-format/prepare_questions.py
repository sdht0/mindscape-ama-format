import json
import argparse
from pathlib import Path

from dotenv import load_dotenv
from baml_client.sync_client import b

load_dotenv()


def load_questions(path: Path) -> list[str]:
    """Use BAML function to parse questions file into summary lines.

    The underlying LLM returns an object with the total count and a list of
    `lines`, where each line contains the name(s) involved and a brief topic
    description. We return the list of lines for downstream processing.
    """

    file_text = path.read_text(encoding="utf-8")

    # Call BAML function ExtractQuestions (defined in baml_src)
    extraction = b.ExtractQuestions(file_text=file_text)
    print(f"LLM extracted {extraction.count} questions from {path.name}")
    if len(extraction.lines) != extraction.count:
        print(
            f"LLM returned {len(extraction.lines)} lines but expected {extraction.count}"
        )
    return list(extraction.lines)


def load_questions_manual(questions_path: Path) -> list[str]:
    data = questions_path.read_text(encoding="utf-8")
    groups: list[str] = []
    current: list[str] = []
    in_group = False
    for line in data.splitlines():
        stripped = line.strip()
        if stripped.startswith("*") and stripped.endswith("*"):
            if in_group:
                groups.append("\n".join(current))
                current = []
                in_group = False
            else:
                in_group = True
        elif not stripped and not in_group:
            if current:
                groups.append("\n".join(current))
                current = []
        elif stripped:
            current.append(stripped)
    if current:
        groups.append(" ".join(current))
    print(f"Loaded {len(groups)} questions from {questions_path.name}")
    return groups


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Format AMA transcript into question/answer sections using BAML."
    )
    parser.add_argument(
        "--questions",
        "-q",
        type=Path,
        help="Path to questions file",
        required=True,
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Path to output file",
        required=True,
    )
    args = parser.parse_args()

    questions_path: Path = args.questions

    if not questions_path.exists():
        raise FileNotFoundError(f"Questions file not found: {questions_path}")

    questions = load_questions_manual(questions_path)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
