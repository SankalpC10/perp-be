from fastapi import FastAPI, HTTPException
from services.web_search import serper_search
from services.ai_service import generate_answer
from services.related_questions import get_related_questions
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
app = FastAPI()
handler = Mangum(app)

origins = [
    # "http://localhost:8000",
    # "http://localhost:3000",
    "https://perp-ai-search.web.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/search")
async def search(query: str):
    res = {}
    contexts = serper_search(query)
    res['contexts'] = contexts
    # names,urls,snippets = fetch_json_attributes(contexts)
    answer = generate_answer(query,contexts)
    res['answer'] = answer
    more_questions = get_related_questions(query,contexts)
    res['more_questions'] = more_questions
    return res
