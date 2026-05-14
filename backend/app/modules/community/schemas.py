
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CommunityPostBase(BaseModel):
    content: str
    post_type: str = "text"
    image_url: Optional[str] = None

class CommunityPostCreate(CommunityPostBase):
    pass

class CommunityPost(CommunityPostBase):
    id: int
    user_id: int
    created_at: datetime
    likes_count: int
    # comments: List[Comment] = [] # simplified for now

    class Config:
        orm_mode = True
