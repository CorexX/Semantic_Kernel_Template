# Instanziiert FastAPI()

# Lädt Config aus core/config.py

# Registriert alle Router aus routers/
import os
from fastapi import FastAPI
from api.routers.agent_registry import router as agent_registry_router

from alembic import command
from alembic.config import Config

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # — Startup —
    app.state.kernel = build_kernel(settings)
    app.state.vita = VitaClient(settings.VITA_API_URL, settings.VITA_API_KEY)

    # Alembic-Migration
    alembic_cfg = Config(os.path.join(os.getcwd(), "alembic.ini"))
    # use replace for sqlite+aiosqlite → sync URL if nötig
    command.upgrade(alembic_cfg, "head")

    yield  # ab hier läuft FastAPI

    # — Shutdown —
    # z.B. Datenbank-Engine oder andere Ressourcen sauber schließen
    # await app.state.db_engine.dispose()  # falls nötig


app = FastAPI()

app.include_router(agent_registry_router)


