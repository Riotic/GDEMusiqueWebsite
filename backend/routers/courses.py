from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import Course, Lesson, Instrument, Enrollment, User
from backend.schemas import (
    CourseResponse, CourseCreate,
    LessonResponse, LessonCreate,
    InstrumentResponse, InstrumentCreate,
    EnrollmentResponse, EnrollmentCreate
)
from backend.routers.auth import get_current_user

router = APIRouter()

# ========== INSTRUMENTS ==========

@router.get("/instruments", response_model=List[InstrumentResponse])
async def get_instruments(db: Session = Depends(get_db)):
    instruments = db.query(Instrument).all()
    return instruments

@router.post("/instruments", response_model=InstrumentResponse, status_code=status.HTTP_201_CREATED)
async def create_instrument(
    instrument: InstrumentCreate,
    db: Session = Depends(get_db)
):
    db_instrument = Instrument(**instrument.dict())
    db.add(db_instrument)
    db.commit()
    db.refresh(db_instrument)
    return db_instrument

# ========== COURSES ==========

@router.get("/", response_model=List[CourseResponse])
async def get_all_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses

@router.get("/my-courses", response_model=List[CourseResponse])
async def get_my_courses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retourne les cours selon les instruments de l'utilisateur"""
    if not current_user.instruments:
        return []
    
    instrument_ids = [inst.id for inst in current_user.instruments]
    courses = db.query(Course).filter(Course.instrument_id.in_(instrument_ids)).all()
    return courses

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

# ========== LESSONS ==========

@router.get("/{course_id}/lessons", response_model=List[LessonResponse])
async def get_course_lessons(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retourne les leçons d'un cours (avec partitions, historique, accords, etc.)"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    lessons = db.query(Lesson).filter(Lesson.course_id == course_id).order_by(Lesson.order).all()
    return lessons

@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
async def get_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retourne une leçon avec partitions, description, historique de la chanson, aide sur les accords"""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.post("/lessons", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
async def create_lesson(
    lesson: LessonCreate,
    db: Session = Depends(get_db)
):
    db_lesson = Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

# ========== ENROLLMENTS ==========

@router.post("/enroll", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll_in_course(
    enrollment: EnrollmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Inscription à un cours"""
    # Vérifier si déjà inscrit
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id,
        Enrollment.course_id == enrollment.course_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")
    
    db_enrollment = Enrollment(
        student_id=current_user.id,
        course_id=enrollment.course_id
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

@router.get("/my-enrollments", response_model=List[EnrollmentResponse])
async def get_my_enrollments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retourne les inscriptions de l'utilisateur"""
    enrollments = db.query(Enrollment).filter(Enrollment.student_id == current_user.id).all()
    return enrollments
