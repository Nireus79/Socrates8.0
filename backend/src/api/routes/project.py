"""Project API routes."""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID

from backend.src.database import get_db
from backend.src.services.project_service import ProjectService
from backend.src.dependencies import get_current_user
from backend.src.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse
from backend.src.models.user import User

router = APIRouter(tags=["projects"])


@router.get("/projects", response_model=ProjectListResponse)
async def list_projects(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status_filter: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List projects owned by current user with pagination."""
    try:
        service = ProjectService(db)

        # Get total count
        total = service.count_projects(owner_id=current_user.id)

        # Get paginated projects
        projects = service.get_projects_paginated(
            owner_id=current_user.id,
            page=page,
            limit=limit,
            status=status_filter
        )

        return {
            "projects": [ProjectResponse.model_validate(p) for p in projects],
            "total": total,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to list projects")


@router.post("/projects", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_project(
    request: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new project for current user."""
    try:
        service = ProjectService(db)
        project = service.create_project(
            name=request.name,
            description=request.description,
            owner_id=current_user.id,
            technology_stack=request.technology_stack or []
        )
        db.commit()

        return {
            "success": True,
            "data": ProjectResponse.model_validate(project),
            "message": "Project created successfully"
        }
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create project")


@router.get("/projects/{project_id}", response_model=dict)
async def get_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get project details by ID."""
    try:
        service = ProjectService(db)
        project = service.get_project_by_id(project_id)

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Check authorization
        if project.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to view this project")

        return {
            "success": True,
            "data": ProjectResponse.model_validate(project),
            "message": "Project retrieved successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve project")


@router.put("/projects/{project_id}", response_model=dict)
async def update_project(
    project_id: UUID,
    request: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update project details."""
    try:
        service = ProjectService(db)
        project = service.get_project_by_id(project_id)

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Check authorization
        if project.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this project")

        # Update fields
        if request.name is not None:
            project.name = request.name
        if request.description is not None:
            project.description = request.description
        if request.status is not None:
            project.status = request.status
        if request.technology_stack is not None:
            project.technology_stack = request.technology_stack

        db.commit()
        db.refresh(project)

        return {
            "success": True,
            "data": ProjectResponse.model_validate(project),
            "message": "Project updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update project")


@router.delete("/projects/{project_id}", response_model=dict)
async def delete_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a project and its associated data."""
    try:
        service = ProjectService(db)
        project = service.get_project_by_id(project_id)

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Check authorization
        if project.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this project")

        # Delete project (cascade will delete sessions and messages)
        service.delete_project(project_id)
        db.commit()

        return {
            "success": True,
            "data": None,
            "message": "Project deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete project")
