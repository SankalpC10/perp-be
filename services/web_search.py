from fastapi import HTTPException
from dotenv import load_dotenv
import json
import requests
import os

load_dotenv()

SERPER_API = os.getenv('SERPER_API')
SERPER_SEARCH_ENDPOINT = os.getenv('SERPER_SEARCH_ENDPOINT')
REFERENCE_COUNT = int(os.getenv('REFERENCE_COUNT'))
DEFAULT_SEARCH_ENGINE_TIMEOUT = int(os.getenv('DEFAULT_SEARCH_ENGINE_TIMEOUT'))


def serper_search(query: str, subscription_key=SERPER_API, prints=False):
    payload = json.dumps({
        "q": query,
        "num": (
            REFERENCE_COUNT
            if REFERENCE_COUNT % 10 == 0
            else (REFERENCE_COUNT // 10 + 1) * 10
        ),
    })
    headers = {'X-API-KEY': subscription_key, "Content-Type": "application/json"}

    try:
        response = requests.post(
            SERPER_SEARCH_ENDPOINT,
            headers=headers,
            data=payload,
            timeout=DEFAULT_SEARCH_ENGINE_TIMEOUT,
        )

        if not response.ok:
            raise HTTPException(status_code=response.status_code, detail="Search engine error.")

        json_content = response.json()
        contexts = [
            {'name': i.get('title'), 'url': i['link'], 'snippet': i['snippet']} for i in json_content.get('organic', [])
        ]

        return contexts

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")
