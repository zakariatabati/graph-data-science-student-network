from fastapi import APIRouter, HTTPException, Query

from app.services.graph_service import graph_service


router = APIRouter(
    prefix="/api/v1/graph",
    tags=["Graph"],
)


@router.get("/stats")
def get_graph_stats():

    stats = graph_service.get_graph_stats()

    return stats


@router.get("/centrality")
def get_centrality(
    metric: str = Query(
        ...,
        enum=[
            "degree",
            "pagerank",
            "betweenness",
            "closeness",
        ],
    ),
    top_k: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
):

    try:
        results = graph_service.get_centrality(
            metric=metric,
            top_k=top_k,
        )

        return {
            "metric": metric,
            "top_k": top_k,
            "results": results,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )