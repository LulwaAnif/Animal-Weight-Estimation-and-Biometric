from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.routes import router

app = FastAPI(title="Grazescale API", version="1.0")

# Optional: allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware to handle large file uploads
@app.middleware("http")
async def add_upload_limit(request: Request, call_next):
    # limit only checked if content-length is present
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 50 * 1024 * 1024:  # 50 MB
        return JSONResponse(
            content={"error": "File too large. Max 50 MB allowed."},
            status_code=413
        )
    return await call_next(request)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to Grazescale - Livestock Morphometric API"}

@app.options("/{rest_of_path:path}")
async def preflight_handler(rest_of_path: str = None):
    """
    Handles browser preflight (OPTIONS) requests globally for CORS.
    """
    return JSONResponse(
        content={"message": "CORS preflight OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )