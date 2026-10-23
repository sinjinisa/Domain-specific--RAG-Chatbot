from groq import Groq

from prompt import NO_ANSWER, SYSTEM_PROMPT
from vector_store import retrieve


GROQ_MODEL = "openai/gpt-oss-20b"


def answer_question(question, index, chunks, api_key):

    matches = retrieve(
        question,
        index,
        chunks,
        top_k=4
    )

    if not matches:
        return NO_ANSWER, []

    context = "\n\n".join(
        f"[Passage {number}]\n"
        f"Document: {item['source']}\n"
        f"Page: {item['page']}\n"
        f"Text: {item['text']}"

        for number, item in enumerate(
            matches, start=1
        )
    )

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=GROQ_MODEL,

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": (
                    f"Context passages:\n{context}"
                    f"\n\nQuestion: {question}"
                )
            }
        ],

        reasoning_effort="low",
        max_completion_tokens=1000,
    )

    answer = (
        response.choices[0].message.content or ""
    ).strip()

    if (
        not answer
        or NO_ANSWER.lower() in answer.lower()
    ):
        return NO_ANSWER, []

    return answer, matches