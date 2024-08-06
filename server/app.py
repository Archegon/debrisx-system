import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .websockets.connection import listen
from .api import api_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the startup event
@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    loop.create_task(listen())

app.include_router(api_router, prefix="/api")