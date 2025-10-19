import string
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import unquote

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    # Decode URL-encoded query
    query = unquote(q).strip().lower()
    # Remove punctuation
    query_clean = query.translate(str.maketrans('', '', string.punctuation))
    
    # Match against cleaned keys
    for key in knowledge_base:
        key_clean = key.lower().translate(str.maketrans('', '', string.punctuation))
        if query_clean == key_clean:
            return knowledge_base[key]
    
    return {"answer": "Sorry, I could not find an exact answer in the TypeScript book.", "sources": None}
