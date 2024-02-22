from pydantic import BaseModel
from typing import List, Optional


class Config(BaseModel):
    api_id: int
    api_hash: str
    bot_token: str
    owner_id: str
    group_id: str | None = None


class Post(BaseModel):
    title: str
    date: str
    url: str
    start_date: str
    end_date: str
    thumbnail: str
    description: str


class Category(BaseModel):
    title: str
    key: str


class HighlightResult(BaseModel):
    value: str
    matchLevel: str
    matchedWords: List[str]


class Article(BaseModel):
    title: str
    description: str
    category: Category
    topics: List[str]
    date_timestamp: int
    start_date_timestamp: int
    end_date_timestamp: int
    thumbnail_url: str
    url: str
    is_old_url: bool
    is_top: bool
    objectID: str
    _highlightResult: Optional[HighlightResult]
