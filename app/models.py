from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Department(Base):
    """Department model - One department has many employees"""
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Relationship: One Department has many Employees
    employees = relationship("Employee", back_populates="department", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Department(id={self.id}, name='{self.name}')>"


class Employee(Base):
    """Employee model - Belongs to one department"""
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(200), nullable=False)
    role = Column(String(100), nullable=False, default="Employee")
    is_active = Column(Boolean, default=True, nullable=False)
    joined_date = Column(DateTime(timezone=True), server_default=func.now())
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)
    
    # Relationship: Employee belongs to one Department
    department = relationship("Department", back_populates="employees")

    def __repr__(self):
        return f"<Employee(id={self.id}, email='{self.email}', full_name='{self.full_name}')>"
