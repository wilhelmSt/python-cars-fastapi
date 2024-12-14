from fastapi import FastAPI
from app.routers.car_router import router as car_router

app = FastAPI(title="Car API", description="API for managing cars", version="1.0")

app.include_router(car_router, prefix="/api", tags=["Cars"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
