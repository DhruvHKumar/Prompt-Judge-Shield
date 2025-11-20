from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import injection, guardrails

app = FastAPI(
    title="AI Security API",
    description="An API to detect and prevent prompt injection attacks.",
    version="1.0.0"
)

origins = [
    "*",  # Allow all origins for Vercel deployment
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(injection.router, prefix="/api/v1/injection", tags=["injection"])
app.include_router(guardrails.router, prefix="/api/v1/guardrails", tags=["guardrails"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Security API"}