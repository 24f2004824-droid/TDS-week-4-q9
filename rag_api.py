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

# Knowledge base with exact excerpts
knowledge_base = {
    "what does the author affectionately call the => syntax": "fat arrow",
    "which operator converts any value into an explicit boolean": "!!",
}

@app.get("/search")
async def search(q: str):
    # Decode query and clean punctuation
    query = unquote(q).strip().lower()
    query_clean = query.translate(str.maketrans('', '', string.punctuation))

    for key, answer in knowledge_base.items():
        key_clean = key.lower().translate(str.maketrans('', '', string.punctuation))
        if query_clean == key_clean:
            return {"answer": answer}

    # Fallback if no match
    return {"answer": "Sorry, I could not find an exact answer in the TypeScript book."}
