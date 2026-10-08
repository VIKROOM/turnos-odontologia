import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine, text

from app.api.routers.turnos import router as turnos_router
from app.config import get_settings

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    settings = get_settings()
    engine = create_engine(settings.database_url)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.info(
        "database connected: %s",
        engine.url.render_as_string(hide_password=True),
    )
    yield
    engine.dispose()


app = FastAPI(title="turnos-odontologia", lifespan=lifespan)
app.include_router(turnos_router)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}
