from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas import DepartmentCreate, DepartmentResponse
from app import crud

router = APIRouter(
    prefix="/departments",
    tags=["departments"]
)


@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    department: DepartmentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new department"""
    # Check if department name already exists
    existing_dept = await crud.get_department_by_name(db, department.name)
    if existing_dept:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Department with name '{department.name}' already exists"
        )
    
    return await crud.create_department(db, department)


@router.get("/", response_model=List[DepartmentResponse])
async def get_departments(db: AsyncSession = Depends(get_db)):
    """Get all departments"""
    return await crud.get_departments(db)


@router.get("/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a department by ID"""
    department = await crud.get_department_by_id(db, department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id {department_id} not found"
        )
    return department
