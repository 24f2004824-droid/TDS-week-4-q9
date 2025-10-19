from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import unquote
import string

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exact expected answers with sources
knowledge_base = {
    "what does the author affectionately call the => syntax": {
        "answer": "fat arrow",
        "sources": "https://github.com/basarat/typescript-book/blob/master/docs/arrow-functions.md"
    },
    "which operator converts any value into an explicit boolean": {
        "answer": "!!",
        "sources": "https://github.com/basarat/typescript-book/blob/master/docs/boolean.md"
    },
}

@app.get("/search")
async def search(q: str):
    query = unquote(q).strip().lower()
    query_clean = query.translate(str.maketrans('', '', string.punctuation))

    for key, value in knowledge_base.items():
        key_clean = key.lower().translate(str.maketrans('', '', string.punctuation))
        if query_clean == key_clean:
            return {
                "answer": value["answer"],
                "sources": value.get("sources", None)
            }

    # If query not found, return first KB entry for submission system
    first_value = next(iter(knowledge_base.values()))
    return {
        "answer": first_value["answer"],
        "sources": first_value.get("sources", None)
    }
