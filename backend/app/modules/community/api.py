
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any
from sqlalchemy.orm import Session
from app.api import deps
from . import models, schemas
from datetime import datetime

router = APIRouter()

@router.post("/posts", response_model=schemas.CommunityPost)
def create_post(
    *,
    db: Session = Depends(deps.get_db),
    post_in: schemas.CommunityPostCreate,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Create a new community post.
    """
    post = models.CommunityPost(
        user_id=current_user.id,
        created_at=datetime.utcnow(),
        **post_in.dict()
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/feed", response_model=List[schemas.CommunityPost])
def get_feed(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 20,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get community feed.
    """
    posts = db.query(models.CommunityPost).order_by(models.CommunityPost.created_at.desc()).offset(skip).limit(limit).all()
    return posts
