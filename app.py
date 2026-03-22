from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from db.database import connect_to_db, close_db_connection
from routers.auth_router import router as AuthRouter
from routers.challenges_router import router as ChallengeRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_db()
    yield
    await close_db_connection()

app = FastAPI(lifespan=lifespan)

@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")

app.include_router(AuthRouter, prefix="/auth", tags=["Auth"], include_in_schema=True)
app.include_router(ChallengeRouter, prefix="/challenges", tags=["Challenges"], include_in_schema=True)