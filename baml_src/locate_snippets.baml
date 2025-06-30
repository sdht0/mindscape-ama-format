function LocateSnippets(question: string, chunk: string) -> Snippets {
  client "openai/gpt-4.1-mini"
  prompt #"
    You will be provided with:
    1. A podcast TRANSCRIPT CHUNK.
    2. Either (i) a single name and a question snipper OR (ii) multiple names and corresponding question snippet, either of which appears somewhere inside the TRANSCRIPT CHUNK.

    Your task:
    • Find the exact location where that question begins inside the chunk.
    • Find the exact location where the question ends and the answer begins.

    Return (i) Whether the question was found, (ii) The first 10 words of the question exactly as they appear in the TRANSCRIPT CHUNK, *including* the asker name and any prefix text such as "let me group these questions", (iii) Whether the answer was found, and (iv) the first 10 words of the answer exactly as they appear in the chunk.

    Verify that the 10 words snippet MUST be a substring in TRANSCRIPT CHUNK without any breaks.

    ---- Example ----
    QUESTION:
    ---
    Eric: I’m missing something about “information”. If one book ... alien language carrying even more insight than the text book?
    ---
    TRANSCRIPT CHUNK:
    ---
    to live either. That's something that you want to get bigger, but you also want to have a pleasurable existence while you are alive. And maybe that involves eating some pizzas. So you have to balance all these things the best you can. Eric says, "I'm missing something about information. If one book was written in gibberish and another with equal amounts of ink and paper, was a quantum mechanics textbook, and both were thrown into a fire, it would take the same amount of information to reconstruct them, if the gibberish were constructed correctly. How can we quantify the additional information in the quantum mechanics book versus gibberish? What if, unbeknownst to us, the gibberish were actually an alien language carrying even more insight than the textbook?" Yeah, these are perfectly good questions. I talk about this a little bit in the big picture, in fact. There's a famous example of the Voynich manuscript,
    ---
    OUTPUT (example not in json):
    question_found = true
    question_snippet = Eric says, "I'm missing something about information. If one book
    answer_found = true
    answer_snippet = Yeah, these are perfectly good questions. I talk about this
    ---- End Example ----

    {{ ctx.output_format }}

    {{ _.role("user") }}
    QUESTION:
    ---
    {{ question }}
    ---

    TRANSCRIPT CHUNK:
    ---
    {{ chunk }}
    ---

    Respond strictly with a JSON object that matches the schema above and no other text.
  "#
}

class Snippets {
  question_found bool @description("Whether the start of the question was found or not")
  question_snippet string @description("First 10 words of the question, verbatim from chunk")
  answer_found bool @description("Whether the start of the answer was found or not")
  answer_snippet string @description("First 10 words of the answer, verbatim from chunk")
}
