from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from backend.database import get_db
from backend.models import ScheduleItem, User, RoleEnum
from backend.schemas import ScheduleItemResponse, ScheduleItemCreate
from backend.routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ScheduleItemResponse])
async def get_my_schedule(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retourne le planning de l'utilisateur connecté
    - Pour un PROFESSEUR: planning complet avec tous ses cours et élèves
    - Pour un ÉLÈVE: planning personnel avec reminders des sujets à bosser
    """
    schedule_items = db.query(ScheduleItem).filter(
        ScheduleItem.user_id == current_user.id
    ).order_by(ScheduleItem.start_time).all()
    
    return schedule_items

@router.get("/week", response_model=List[ScheduleItemResponse])
async def get_week_schedule(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retourne le planning de la semaine en cours"""
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)
    
    schedule_items = db.query(ScheduleItem).filter(
        ScheduleItem.user_id == current_user.id,
        ScheduleItem.start_time >= start_of_week,
        ScheduleItem.start_time < end_of_week
    ).order_by(ScheduleItem.start_time).all()
    
    return schedule_items

@router.get("/upcoming", response_model=List[ScheduleItemResponse])
async def get_upcoming_schedule(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retourne les prochains événements du planning"""
    now = datetime.now()
    
    schedule_items = db.query(ScheduleItem).filter(
        ScheduleItem.user_id == current_user.id,
        ScheduleItem.start_time >= now
    ).order_by(ScheduleItem.start_time).limit(10).all()
    
    return schedule_items

@router.post("/", response_model=ScheduleItemResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule_item(
    schedule_item: ScheduleItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Créer un événement dans le planning"""
    is_teacher_view = current_user.role == RoleEnum.TEACHER
    
    db_schedule_item = ScheduleItem(
        **schedule_item.dict(),
        user_id=current_user.id,
        is_teacher_view=is_teacher_view
    )
    db.add(db_schedule_item)
    db.commit()
    db.refresh(db_schedule_item)
    return db_schedule_item

@router.put("/{item_id}", response_model=ScheduleItemResponse)
async def update_schedule_item(
    item_id: int,
    schedule_update: ScheduleItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Modifier un événement du planning"""
    db_item = db.query(ScheduleItem).filter(
        ScheduleItem.id == item_id,
        ScheduleItem.user_id == current_user.id
    ).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Schedule item not found")
    
    for key, value in schedule_update.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Supprimer un événement du planning"""
    db_item = db.query(ScheduleItem).filter(
        ScheduleItem.id == item_id,
        ScheduleItem.user_id == current_user.id
    ).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Schedule item not found")
    
    db.delete(db_item)
    db.commit()
    return None

@router.get("/students", response_model=List[dict])
async def get_teacher_students(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retourne la liste des élèves d'un professeur (TEACHER uniquement)"""
    if current_user.role != RoleEnum.TEACHER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can access student list"
        )
    
    # Récupérer les cours enseignés par le professeur
    from backend.models import Enrollment
    
    students_data = []
    for course in current_user.taught_courses:
        enrollments = db.query(Enrollment).filter(Enrollment.course_id == course.id).all()
        for enrollment in enrollments:
            student = enrollment.student
            students_data.append({
                "id": student.id,
                "username": student.username,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "email": student.email,
                "course": course.title,
                "progress": enrollment.progress
            })
    
    return students_data
