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

# Knowledge base (example from TypeScript book)
knowledge_base = {
    "what does the author affectionately call the => syntax": "fat arrow",
    "which operator converts any value into an explicit boolean": "!!",
    # Add more Q&A here if needed
}

# Root redirects to /search
@app.get("/")
async def root():
    return RedirectResponse(url="/search")

# Search endpoint: always returns JSON
@app.get("/search")
async def search(q: str = None):
    if q:
        query = unquote(q).strip().lower()
        query_clean = query.translate(str.maketrans('', '', string.punctuation))

        for key, answer in knowledge_base.items():
            key_clean = key.lower().translate(str.maketrans('', '', string.punctuation))
            if query_clean == key_clean:
                return {"answer": answer}

        # If query does not match anything
        return {"answer": "Sorry, I could not find an exact answer in the TypeScript book."}
    
    # If no query provided, return a default answer
    return {"answer": "Please provide a question, or try any question about TypeScript!"}
