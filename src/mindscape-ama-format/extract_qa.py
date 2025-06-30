import json
import re
import argparse
from pathlib import Path
import time

from baml_client.sync_client import b
from dotenv import load_dotenv

load_dotenv()


CHUNK_SIZE = 10000

DELIM_Q = "\n--\n"
DELIM_A = "\n\n"


def locate_substring(snippet: str, chunk: str) -> int:
    pattern = re.escape(snippet[:50])
    match = re.search(pattern, chunk, flags=re.IGNORECASE)
    return match.start() if match else -1


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

    transcript_path: Path = args.transcript
    questions_path: Path = args.questions

    if not transcript_path.exists():
        raise FileNotFoundError(f"Transcript file not found: {transcript_path}")
    if not questions_path.exists():
        raise FileNotFoundError(f"Questions file not found: {questions_path}")

    transcript = transcript_path.read_text(encoding="utf-8")
    print(f"Loaded transcript of {len(transcript)} characters.")

    questions = json.load(questions_path.open(encoding="utf-8"))
    print(f"Loaded {len(questions)} questions/groups.")

    if args.output.exists():
        with open(args.output, "r", encoding="utf-8") as f:
            found = json.load(f)
    else:
        found = {}

    for index in range(len(questions)):
        print(f"Processing question {index}...")
        if str(index) not in found:
            print("Sleeping for 1 seconds...")
            time.sleep(1)
            prev_answer_index = (
                found[str(index - 1)]["answer_start"] if index > 0 else 0
            )
            question = questions[index]
            found_question = False
            for chunk_size in [5000, 7000, 8000, 10000]:
                chunk = transcript[prev_answer_index : prev_answer_index + chunk_size]
                snippets = b.LocateSnippets(question=question, chunk=chunk)
                data = {
                    "question_found": snippets.question_found,
                    "answer_found": snippets.answer_found,
                    "question_snippet": snippets.question_snippet,
                    "answer_snippet": snippets.answer_snippet,
                }
                if data["question_found"] and data["answer_found"]:
                    question_index = locate_substring(
                        data["question_snippet"], transcript
                    )
                    if question_index == -1:
                        print(
                            f"{index}: Question '{data['question_snippet']}' not found in transcript."
                        )
                        break
                    answer_index = locate_substring(data["answer_snippet"], transcript)
                    if answer_index == -1:
                        print(
                            f"{index}: Answer '{data['answer_snippet']}' not found in transcript."
                        )
                        break
                    data["question_start"] = question_index
                    data["answer_start"] = answer_index
                    found[str(index)] = data
                    with open(args.output, "w", encoding="utf-8") as f:
                        json.dump(found, f, indent=2, ensure_ascii=False)
                    found_question = True
                    break
                else:
                    print(f"Question {index} not found, trying again.")
            if not found_question:
                print(f"Stopping at question {index} because it was not found.")
                break

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(found, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
