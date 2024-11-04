from services.ai_service import Groq_query

_more_questions_prompt = """
You are a helpful assistant that helps the user to ask related questions, based on user's original question and the related contexts. Please identify worthwhile topics that can be follow-ups, and write questions no longer than 20 words each. Please make sure that specifics, like events, names, locations, are included in follow up questions so they can be asked standalone. For example, if the original question asks about "the Manhattan project", in the follow up question, do not just say "the project", but use the full name "the Manhattan project". The format of giving the responses and generating the questions should be like this:
1. [Question 1]
2. [Question 2]
3. [Question 3]
Here are the contexts of the question:
{context}
"""

def get_related_questions(query,contexts):
    system_prompt = _more_questions_prompt.format(
        context="\n\n".join([c["snippet"] for c in contexts])
    )
    try:
        complete_responses = Groq_query(system_prompt,query)
        return complete_responses
    except Exception as e:
        print(e)
        return []