import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.qr.router import router as qr_router
from src.ascii.router import router as ascii_router

app = FastAPI()

origins = [
    "https://00rei.tech",
    "https://api.00rei.tech",
    "http://localhost",
    "https://localhost",
    "https://localhost:8000",
    "http://localhost:8000",
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.include_router(ascii_router)
app.include_router(qr_router)


@app.get("/")
async def root():
    return {"00rei.tech": "✅"}
