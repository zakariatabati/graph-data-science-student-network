from typing import List, Optional

from pydantic import BaseModel


class FriendRecommendation(BaseModel):
    student_id: str
    score: float
    student_name: Optional[str] = None
    
class FriendRecommendationResponse(BaseModel):
    student_id: str
    method: str
    top_k: int
    recommendations: List[FriendRecommendation]




class ClubRecommendation(BaseModel):
    club_id: str
    name: Optional[str] = None


class ClubRecommendationResponse(BaseModel):
    student_id: str
    recommendations: List[ClubRecommendation]


class EventRecommendation(BaseModel):
    event_id: str
    name: Optional[str] = None

class EventRecommendationResponse(BaseModel):
    student_id: str
    recommendations: List[EventRecommendation]