# import sys
# from pathlib import Path
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from avito.api import router as api_router

# sys.path.append(str(Path(__file__).parent.parent))
from avito.core.config import settings
from avito.core.db_init import init_merch_items
from avito.core.models import db_helper


@asynccontextmanager
async def get_session():
    """Обёртка для использования session_getter() с async with"""
    session_generator = db_helper.session_getter()
    session = await anext(session_generator)  # Получаем первую сессию
    try:
        yield session
    finally:
        await session.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    async with get_session() as session:
        await init_merch_items(session)
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    title="API Avito shop",
    version="1.0.0",
    openapi_url="/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    debug=False,
)
main_app.include_router(
    api_router,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
