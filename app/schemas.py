from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# =============== Department Schemas ===============

class DepartmentBase(BaseModel):
    """Base schema for Department"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    """Schema for creating a new department"""
    pass


class DepartmentResponse(DepartmentBase):
    """Schema for department response"""
    id: int

    class Config:
        from_attributes = True


class DepartmentWithEmployees(DepartmentResponse):
    """Schema for department with employees list"""
    employees: List["EmployeeResponse"] = []

    class Config:
        from_attributes = True


# =============== Employee Schemas ===============

class EmployeeBase(BaseModel):
    """Base schema for Employee"""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=200)
    role: str = Field(default="Employee", max_length=100)
    is_active: bool = True
    department_id: int


class EmployeeCreate(EmployeeBase):
    """Schema for creating a new employee"""
    pass


class EmployeeResponse(BaseModel):
    """Schema for employee response"""
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    joined_date: datetime
    department_id: int

    class Config:
        from_attributes = True


class EmployeeWithDepartment(EmployeeResponse):
    """Schema for employee with department details"""
    department: DepartmentResponse

    class Config:
        from_attributes = True


# Update forward references for circular dependency
DepartmentWithEmployees.model_rebuild()
