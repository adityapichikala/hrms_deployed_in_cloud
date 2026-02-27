from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.models import Department, Employee
from app.schemas import DepartmentCreate, EmployeeCreate


# =============== Department CRUD ===============

async def create_department(db: AsyncSession, department: DepartmentCreate) -> Department:
    """Create a new department"""
    db_department = Department(**department.model_dump())
    db.add(db_department)
    await db.commit()
    await db.refresh(db_department)
    return db_department


async def get_departments(db: AsyncSession) -> List[Department]:
    """Get all departments"""
    result = await db.execute(select(Department))
    return result.scalars().all()


async def get_department_by_id(db: AsyncSession, department_id: int) -> Optional[Department]:
    """Get a department by ID"""
    result = await db.execute(
        select(Department).where(Department.id == department_id)
    )
    return result.scalar_one_or_none()


async def get_department_by_name(db: AsyncSession, name: str) -> Optional[Department]:
    """Get a department by name"""
    result = await db.execute(
        select(Department).where(Department.name == name)
    )
    return result.scalar_one_or_none()


# =============== Employee CRUD ===============

async def create_employee(db: AsyncSession, employee: EmployeeCreate) -> Employee:
    """Create a new employee"""
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    await db.commit()
    await db.refresh(db_employee)
    return db_employee


async def get_employees(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Employee]:
    """Get all employees with pagination"""
    result = await db.execute(
        select(Employee)
        .options(selectinload(Employee.department))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_employee_by_id(db: AsyncSession, employee_id: int) -> Optional[Employee]:
    """Get an employee by ID"""
    result = await db.execute(
        select(Employee)
        .options(selectinload(Employee.department))
        .where(Employee.id == employee_id)
    )
    return result.scalar_one_or_none()


async def get_employee_by_email(db: AsyncSession, email: str) -> Optional[Employee]:
    """Get an employee by email"""
    result = await db.execute(
        select(Employee).where(Employee.email == email)
    )
    return result.scalar_one_or_none()
