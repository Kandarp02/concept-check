from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Concept Check API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

IDEAS = [
    {"id": 1, "title": "Why does a backend exist at all?"},
    {"id": 2, "title": "What does one API call carry?"},
    {"id": 3, "title": "Why can't the key live in the browser?"},
    {"id": 4, "title": "Why does the app forget without storage?"},
    {"id": 5, "title": "Why does the pointer sit on the many side?"},
    {"id": 6, "title": "Why is history a row, not a cell?"},
    {"id": 7, "title": "How do you decide where a piece lives?"},
]


# ── /api prefixed routes ─────────────────────────────────────────────────────

@app.get("/api/health")
async def api_health():
    return {"ok": True}


@app.get("/api/ideas")
async def api_ideas():
    return IDEAS


# ── unprefixed mirrors ───────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"ok": True}


@app.get("/ideas")
async def ideas():
    return IDEAS


# ── root – serve index.html ──────────────────────────────────────────────────

def _find_index_html():
    """Search common locations — works locally and on Vercel."""
    base = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base, "..", "public", "index.html"),  # local dev
        os.path.join(base, "..", "index.html"),            # repo root
        os.path.join(base, "index.html"),                   # same dir
    ]
    for p in candidates:
        if os.path.isfile(p):
            return p
    return None


@app.get("/")
async def index():
    path = _find_index_html()
    if path:
        with open(path, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    return JSONResponse(status_code=404, content={"detail": "index.html not found", "searched_from": os.path.dirname(os.path.abspath(__file__))})


# ── catch-all (must be last) ─────────────────────────────────────────────────

@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
)
async def catch_all(request: Request, path: str):
    return JSONResponse(
        status_code=404,
        content={"detail": "no route matched", "seen_path": str(request.url.path)},
    )


if __name__ == "__main__":
    import uvicorn

    # Works from inside api/  →  python index.py
    # Works from repo root    →  python api/index.py
    uvicorn.run("index:app", host="0.0.0.0", port=8000, reload=True)
