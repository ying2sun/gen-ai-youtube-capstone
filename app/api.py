from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from MobileSummarizer import VideoSummarizer
from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
API_AUTH_KEY = "********"   # required key to interact

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

summarizer = VideoSummarizer(
    api_key=OPENROUTER_API_KEY,
    apify_token=APIFY_TOKEN
)

class SummarizeRequest(BaseModel):
    video_url: str

# ******* AUTH MIDDLEWARE *******
@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    if request.url.path not in ["/", "/docs", "/openapi.json"]:
        api_key = request.headers.get("X-API-Key")
        if api_key != API_AUTH_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")
    return await call_next(request)
# ********************************

@app.post("/summarize")
def summarize_video(request: SummarizeRequest):
    summary = summarizer.generate_summary(request.video_url)
    return {"summary": summary}

@app.get("/")
def root():
    return {"status": "API running", "auth": "protected"}
