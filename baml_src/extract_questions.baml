 function ExtractQuestions(file_text: string) -> QuestionExtraction {
  client OllamaClient
  prompt #"
    The following text lists single questions and question groups from a podcast AMA transcript.
    Single question consist of just a name and a question.
    Question group consist of multiple names and questions, all surrounded by asterisks.

    Your tasks:
    1. Count how many single questions + question groups there are.
       All questions within asterisks are considered to be part of the SAME question.
    2. For each question/group, produce a ONE-LINE summary consisting of:
       - The name(s) mentioned in the question.
       - A short topic description (6-12 words) for quick reference.
    The number of lines in step 2 should EXACTLY match the count from step 1.
    Example line: "Alice & Bob: career trajectory and early challenges"

    Output strictly as JSON according to the output schema below and NOTHING else.

    {{ ctx.output_format }}

    {{ _.role("user") }}
    --- BEGIN QUESTIONS FILE ---
    {{ file_text }}
    --- END QUESTIONS FILE ---
  "#
}

class QuestionExtraction {
  count int @description("Total number of questions or question groups found")
  lines string[] @description("Array of one-line summaries, one per question/group, length == count")
}
