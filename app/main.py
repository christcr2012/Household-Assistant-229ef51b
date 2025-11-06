from __future__ import annotations

from fastapi import FastAPI

from app.api import assistant, auth, calendar, email, inventory
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Robinson Household Assistant")

app.include_router(auth.router)
app.include_router(assistant.router)
app.include_router(calendar.router)
app.include_router(email.router)
app.include_router(inventory.router)


@app.get("/health")
def healthcheck():
    return {"status": "ok"}
