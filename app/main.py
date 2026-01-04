from fastapi import FastAPI
from app.api.webhook import router as webhook_router

app = FastAPI(
    title="WhatsApp Sales Agent",
    version="0.1.0"
)

# Routes
app.include_router(webhook_router)

@app.get("/")
def health_check():
    return {"status": "ok"}
