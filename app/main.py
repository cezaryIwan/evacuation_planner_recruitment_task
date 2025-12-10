from fastapi import FastAPI
from app.api.evac_router import router as evac_router

app = FastAPI()

app.include_router(evac_router)