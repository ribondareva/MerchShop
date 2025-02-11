from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from core.config import settings
from api import router as api_router
from core.models import db_helper, Base


# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from database import get_db
# from models import User
# from auth import (
#     create_access_token,
#     hash_password,
#     verify_password,
#     decode_access_token,
# )
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(
    api_router,
    prefix=settings.api.prefix,
)
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
#
#
# # Регистрация нового пользователя
# @app.post("/auth/register")
# async def register_user(
#     username: str, password: str, db: AsyncSession = Depends(get_db)
# ):
#     async with db as session:
#         result = await session.execute(select(User).where(User.username == username))
#         existing_user = result.scalars().first()
#
#         if existing_user:
#             raise HTTPException(status_code=400, detail="Username already exists")
#
#         new_user = User(username=username, hashed_password=hash_password(password))
#         session.add(new_user)
#         await session.commit()
#         return {"message": "User registered successfully"}
#
#
# # Авторизация (выдача JWT-токена)
# @app.post("/auth/token")
# async def login_user(
#     form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
# ):
#     async with db as session:
#         result = await session.execute(
#             select(User).where(User.username == form_data.username)
#         )
#         user = result.scalars().first()
#
#         if not user or not verify_password(form_data.password, user.hashed_password):
#             raise HTTPException(status_code=401, detail="Invalid credentials")
#
#         access_token = create_access_token({"sub": user.username})
#         return {"access_token": access_token, "token_type": "bearer"}
#
#
# # Получение текущего пользователя по JWT
# async def get_current_user(
#     token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
# ):
#     payload = decode_access_token(token)
#     if not payload:
#         raise HTTPException(status_code=401, detail="Invalid token")
#
#     username: str = payload.get("sub")
#     async with db as session:
#         result = await session.execute(select(User).where(User.username == username))
#         user = result.scalars().first()
#
#         if not user:
#             raise HTTPException(status_code=401, detail="User not found")
#
#     return user
#
#
# @app.get("/users/me")
# async def get_my_profile(current_user: User = Depends(get_current_user)):
#     return {"username": current_user.username, "balance": current_user.balance}
if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
