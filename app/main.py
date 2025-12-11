from fastapi import FastAPI
from app.api.evac_router import router as evac_router

app = FastAPI()

app.include_router(evac_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)