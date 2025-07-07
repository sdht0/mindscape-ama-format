# Mindscape AMA Formatter

I'm [maintaining an archive](https://docs.google.com/spreadsheets/d/1i2tmn7L-nlqOz0i-O1MVoOg6kafe9gC45VkaXs0LxMA/edit?gid=1378547435#gid=1378547435)
of all AMA questions and answers discussed in the [Mindscape podcast](https://www.preposterousuniverse.com/podcast/).
Initially, I was creating the archive mostly manually.
But why continue to do that when LLMs have become so skillfull at understanding language.

This repository leverages LLM models to automatically identify and split the transcripts into individual questions and answers.

Using the wonderful [BAML](https://github.com/BoundaryML/baml) library to prompt the LLM and get structured outputs without any manual parsing.

## Prerequisites

* Install the required libraries:

```bash
uv sync --extra dev
```

* An **OpenAI API key**:

```bash
echo OPENAI_API_KEY="sk-..." > .env
```

## Needed files from the AMA description page

* `raw.txt` – Raw transcript copied from the AMA description page.
* `questions.txt` – Raw questions list copied from the AMA description page.

## Usage

```bash
cat ./files/raw.txt | tr '\n' '-' | sed -r -e 's/-+[0-9\:\.]+ (S.?|Sean Carroll): / /g' > ./files/ama.txt
# Best to remove the intro and outro from the raw transcript manually.
uv run python src/mindscape-ama-format/prepare_questions.py \
   -q ./files/questions.txt -o ./files/questions.json
uv run python src/mindscape-ama-format/extract_qa.py \
   -t ./files/ama.txt -q ./files/questions.json -o ./files/output.json
uv run python src/mindscape-ama-format/final_output.py \
   -t ./files/ama.txt -i ./files/output.json -y 2025.06 -o ./files/qa.csv
```

The script will:

1. Parse `questions.txt` to prepare a list of individual and grouped questions.
2. For each question, find the corresponding question and answer snippet in `ama.txt` using an LLM.
3. Search for the snippets in `ama.txt` to figure out the boundaries and save them to a csv file.
