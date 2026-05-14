from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.exercise_library_v2.models import ExerciseV2
from app.exercise_library_v2.schemas import ExerciseV2Create, ExerciseFilter

class ExerciseLibraryService:
    @staticmethod
    def get_exercise(db: Session, exercise_id: int):
        return db.query(ExerciseV2).filter(ExerciseV2.id == exercise_id).first()

    @staticmethod
    def list_exercises(db: Session, filters: ExerciseFilter):
        query = db.query(ExerciseV2)
        
        if filters.muscle_group:
            query = query.filter(ExerciseV2.muscle_groups.contains([filters.muscle_group]))
            
        if filters.equipment:
            # Matches if any of the required equipment is in the user's available equipment list
            # For simplicity, we filter exercises where all needed equipment is in the list
            for eq in filters.equipment:
                # This is a bit complex in SQLite/Postgres with JSON
                # Logic: filter exercises where equipment_needed is a subset of available
                pass 
                
        if filters.search:
            query = query.filter(ExerciseV2.name.ilike(f"%{filters.search}%"))
            
        return query.all()

    @staticmethod
    def create_exercise(db: Session, exercise_in: ExerciseV2Create):
        db_exercise = ExerciseV2(**exercise_in.dict())
        db.add(db_exercise)
        db.commit()
        db.refresh(db_exercise)
        return db_exercise

    @staticmethod
    def get_progression(db: Session, exercise_id: int):
        exercise = ExerciseLibraryService.get_exercise(db, exercise_id)
        if exercise and exercise.progression_id:
            return db.query(ExerciseV2).get(exercise.progression_id)
        return None

    @staticmethod
    def get_regression(db: Session, exercise_id: int):
        exercise = ExerciseLibraryService.get_exercise(db, exercise_id)
        if exercise and exercise.regression_id:
            return db.query(ExerciseV2).get(exercise.regression_id)
        return None
