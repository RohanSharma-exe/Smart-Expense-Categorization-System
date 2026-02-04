from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="Smart Expense Categorization System", version="0.1.0")
app.include_router(router, prefix="/v1")


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
