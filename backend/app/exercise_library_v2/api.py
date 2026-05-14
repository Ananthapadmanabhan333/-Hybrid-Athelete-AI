from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api import deps
from app.exercise_library_v2.schemas import ExerciseV2Out, ExerciseV2Create, ExerciseFilter
from app.exercise_library_v2.services import ExerciseLibraryService

router = APIRouter()

@router.get("/", response_model=List[ExerciseV2Out])
def get_exercises(
    muscle_group: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(deps.get_db)
):
    filters = ExerciseFilter(muscle_group=muscle_group, search=search)
    return ExerciseLibraryService.list_exercises(db, filters)

@router.get("/{exercise_id}", response_model=ExerciseV2Out)
def get_exercise(
    exercise_id: int,
    db: Session = Depends(deps.get_db)
):
    exercise = ExerciseLibraryService.get_exercise(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@router.post("/", response_model=ExerciseV2Out)
def create_exercise(
    exercise_in: ExerciseV2Create,
    db: Session = Depends(deps.get_db)
):
    return ExerciseLibraryService.create_exercise(db, exercise_in)

@router.get("/{exercise_id}/progression", response_model=Optional[ExerciseV2Out])
def get_progression(
    exercise_id: int,
    db: Session = Depends(deps.get_db)
):
    return ExerciseLibraryService.get_progression(db, exercise_id)

@router.get("/{exercise_id}/regression", response_model=Optional[ExerciseV2Out])
def get_regression(
    exercise_id: int,
    db: Session = Depends(deps.get_db)
):
    return ExerciseLibraryService.get_regression(db, exercise_id)
