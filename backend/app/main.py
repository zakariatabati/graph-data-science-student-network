from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.repositories.neo4j import neo4j_repository
from app.routers.recommendations import router as recommendations_router
from app.routers.communities import router as communities_router
from app.routers.students import router as students_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    neo4j_repository.close()


app = FastAPI(
    title="Student Social Network GDS API",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(recommendations_router)
app.include_router(communities_router)
app.include_router(students_router)

@app.get("/")
def root():
    return {
        "message": "Student Social Network GDS API is running"
    }