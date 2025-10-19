from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from urllib.parse import unquote
import string

app = FastAPI(title="TypeScript RAG API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Knowledge base
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

# Root redirects to /search
@app.get("/")
async def root():
    return RedirectResponse(url="/search")

# Search endpoint with default query
@app.get("/search")
async def search(q: str = "What does the author affectionately call the => syntax"):
    # Decode URL-encoded query
    query = unquote(q).strip().lower()
    # Remove punctuation
    query_clean = query.translate(str.maketrans('', '', string.punctuation))
    
    # Match against knowledge base
    for key in knowledge_base:
        key_clean = key.lower().translate(str.maketrans('', '', string.punctuation))
        if query_clean == key_clean:
            return knowledge_base[key]
    
    # Fallback
    return {"answer": "Sorry, I could not find an exact answer in the TypeScript book.", "sources": None}
