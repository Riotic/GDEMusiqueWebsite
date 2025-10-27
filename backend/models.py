from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base
import enum

# Table d'association pour les instruments d'un utilisateur
user_instruments = Table(
    'user_instruments',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('instrument_id', Integer, ForeignKey('instruments.id'), primary_key=True)
)

# Table d'association pour les cours d'un professeur
teacher_courses = Table(
    'teacher_courses',
    Base.metadata,
    Column('teacher_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True)
)

class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relations
    instruments = relationship("Instrument", secondary=user_instruments, back_populates="users")
    enrollments = relationship("Enrollment", back_populates="student")
    taught_courses = relationship("Course", secondary=teacher_courses, back_populates="teachers")
    schedule_items = relationship("ScheduleItem", back_populates="user")

class Instrument(Base):
    __tablename__ = "instruments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    image_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    users = relationship("User", secondary=user_instruments, back_populates="instruments")
    courses = relationship("Course", back_populates="instrument")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False)
    level = Column(String(50))  # Débutant, Intermédiaire, Avancé
    image_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relations
    instrument = relationship("Instrument", back_populates="courses")
    lessons = relationship("Lesson", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    teachers = relationship("User", secondary=teacher_courses, back_populates="taught_courses")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    song_name = Column(String(200))
    song_history = Column(Text)
    chord_help = Column(Text)
    sheet_music_url = Column(String(500))
    video_url = Column(String(500))
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relations
    course = relationship("Course", back_populates="lessons")

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    progress = Column(Integer, default=0)  # Pourcentage de progression

    # Relations
    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class MarketplaceItem(Base):
    __tablename__ = "marketplace_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    image_url = Column(String(500))
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_sold = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relations
    seller = relationship("User")

class ScheduleItem(Base):
    __tablename__ = "schedule_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"))
    reminder_text = Column(Text)  # Sujets à bosser pour la semaine
    is_teacher_view = Column(Boolean, default=False)  # Pour différencier vue prof/élève
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relations
    user = relationship("User", back_populates="schedule_items")
    course = relationship("Course")
