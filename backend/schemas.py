from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from backend.models import RoleEnum

# Instrument Schemas (défini en premier pour éviter les forward refs)
class InstrumentBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class InstrumentCreate(InstrumentBase):
    pass

class InstrumentResponse(InstrumentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: Optional[RoleEnum] = RoleEnum.USER

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    role: RoleEnum
    is_active: bool
    created_at: datetime
    instruments: List[InstrumentResponse] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Course Schemas
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    instrument_id: int
    level: Optional[str] = "Débutant"
    image_url: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    created_at: datetime
    instrument: InstrumentResponse

    class Config:
        from_attributes = True

# Lesson Schemas
class LessonBase(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    song_name: Optional[str] = None
    song_history: Optional[str] = None
    chord_help: Optional[str] = None
    sheet_music_url: Optional[str] = None
    video_url: Optional[str] = None
    order: int = 0

class LessonCreate(LessonBase):
    pass

class LessonResponse(LessonBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Enrollment Schemas
class EnrollmentCreate(BaseModel):
    course_id: int

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime
    progress: int
    course: CourseResponse

    class Config:
        from_attributes = True

# Marketplace Schemas
class MarketplaceItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    image_url: Optional[str] = None

class MarketplaceItemCreate(MarketplaceItemBase):
    pass

class MarketplaceItemResponse(MarketplaceItemBase):
    id: int
    seller_id: int
    is_sold: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Schedule Schemas
class ScheduleItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    course_id: Optional[int] = None
    reminder_text: Optional[str] = None

class ScheduleItemCreate(ScheduleItemBase):
    pass

class ScheduleItemResponse(ScheduleItemBase):
    id: int
    user_id: int
    is_teacher_view: bool
    created_at: datetime

    class Config:
        from_attributes = True
