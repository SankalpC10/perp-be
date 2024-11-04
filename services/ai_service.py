import groq
import re
import os
from dotenv import load_dotenv

load_dotenv()

client = groq.Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def Groq_query(system_prompt,query):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": query,
        }
    ],
    model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

_rag_query_text = """
"You are a large language AI assistant tasked with providing a clean, concise, and accurate answer to the user question. Your response must rely strictly on the context provided, each starting with a reference number like [[citation:x]], where x is a number. Use these contexts to substantiate every factual statement with citations directly following each applicable sentence.
For each sentence with relevant information, include a citation in the format [citation:x] to indicate sourced material. If multiple contexts apply, include all relevant citations like [citation:3][citation:5]. If the information provided is incomplete, say 'information is missing on' followed by the related topic. If a sentence can’t be substantiated by a specific context, avoid making assumptions or adding unsourced information.
Every paragraph should end with at least one citation, summarizing the main sources referenced within it.
If any required information is missing, specify this clearly in your answer.
Write with an unbiased, professional tone, limiting your response to 500 words.
User Question: {context}
Example answer: 'Answer [citation:1][citation:2][citation:3].'
Follow this citation style strictly throughout the response."
"""


def generate_answer(query, contexts):
    query = re.sub(r"\[/?INST\]", "", query)

    system_prompt = _rag_query_text.format(
        context="\n\n".join(
            [f"[[citation:{i + 1}]]{c['snippet']}" for i, c in enumerate(contexts)]
        )
    )

    try:
        complete_response = Groq_query(system_prompt, query)
        return complete_response
    except Exception as e:
        print(e)
        return "Failed Response"