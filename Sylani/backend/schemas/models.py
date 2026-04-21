# models.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserSignup(BaseModel):
    email: EmailStr
    password: str

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str

class ForgotPasswordSchema(BaseModel):
    email: EmailStr

class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str


class ArticleRequest(BaseModel):
    title: str
    content: str = ""
    
class Process(BaseModel):
    user_id: str
    step: int
    data: dict
    completed: Optional[bool] = False

class KeywordRequest(BaseModel):
    text: str

class SentimentRequest(BaseModel):
    text: str


class TrendResponse(BaseModel):
    keyword: str
    count: int


class InsightResponse(BaseModel):
    total_articles: int
    positive: int
    negative: int
    neutral: int


class SearchResponse(BaseModel):
    title: str
    source: str
    url: str


class SummaryResponse(BaseModel):
    total_articles: int
    avg_relevance: float
    top_keywords: List[str]