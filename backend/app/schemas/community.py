from typing import Literal

from pydantic import BaseModel


CommunityAlgorithm = Literal[
    "louvain",
    "leiden",
    "label_propagation",
]


class CommunityDetectionRequest(BaseModel):
    algorithm: CommunityAlgorithm


class CommunityResponse(BaseModel):
    community_id: int
    size: int


class CommunityDetailResponse(BaseModel):
    community_id: int
    students: list[dict]


class CommunityComparisonResponse(BaseModel):
    algorithm: str
    community_count: int
    modularity: float | None = None
    execution_time: float | None = None