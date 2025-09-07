from fastapi import FastAPI, Form, Request, status, Security, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security.api_key import APIKeyHeader
import uvicorn
import os

# Get API key from environment variable or use a default for development
API_KEY = os.environ.get("API_KEY", "default-dev-key-change-in-production")
API_KEY_NAME = "X-API-Key"

# Setup API key authentication
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key"
    )

app = FastAPI()

# Public endpoint - no authentication required
@app.get("/")
def public_endpoint():
    return {
        "message": "This is a public endpoint. To access the protected endpoint, use /hello with an X-API-Key header."
    }

# Protected endpoint with API key authentication
@app.get("/hello")
def say_hello(api_key: str = Depends(get_api_key)):
    return {"message": "Hello, welcome to FastAPI!"}

