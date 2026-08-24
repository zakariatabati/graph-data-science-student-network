from typing import List

from pydantic import BaseModel


class FriendRecommendation(BaseModel):
    student_id: str
    score: float
    student_name: str
    
class FriendRecommendationResponse(BaseModel):
    student_id: str
    method: str
    top_k: int
    recommendations: List[FriendRecommendation]




class ClubRecommendation(BaseModel):
    club_id: str
    name: str


class ClubRecommendationResponse(BaseModel):
    student_id: str
    recommendations: List[ClubRecommendation]


class EventRecommendation(BaseModel):
    event_id: str
    name: str

class EventRecommendationResponse(BaseModel):
    student_id: str
    recommendations: List[EventRecommendation]