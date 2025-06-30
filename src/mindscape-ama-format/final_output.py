import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Format AMA transcript into question/answer sections using BAML."
    )
    parser.add_argument(
        "--transcript",
        "-t",
        type=Path,
        help="Path to transcript file",
        required=True,
    )
    parser.add_argument(
        "--index",
        "-i",
        type=Path,
        help="Path to output file",
        required=True,
    )
    parser.add_argument(
        "--year",
        "-y",
        type=str,
        help="Year of the AMA",
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

    # Read the transcript file
    transcript = args.transcript.read_text(encoding="utf-8")

    with open(args.index, "r", encoding="utf-8") as f:
        indices = json.load(f)

    for index, data in indices.items():
        question_snippet = data["question_snippet"]
        answer_snippet = data["answer_snippet"]
        transcript = transcript.replace(
            question_snippet, f"\n{args.year}\t{int(index) + 1}\t{question_snippet}"
        )
        transcript = transcript.replace(answer_snippet, f"\t{answer_snippet}")

    args.output.write_text(transcript, encoding="utf-8")


if __name__ == "__main__":
    main()
