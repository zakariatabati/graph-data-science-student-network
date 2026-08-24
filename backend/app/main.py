from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.repositories.neo4j import neo4j_repository


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    neo4j_repository.close()


app = FastAPI(
    title="Student Social Network GDS API",
    description="API for graph analysis and recommendation algorithms",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "message": "Student Social Network GDS API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }