import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func, col

from app.dependencies import get_db, get_current_user, verify_user_ownership
from app.exceptions import NotFoundError
from app.models import User, Task
from app.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse

router = APIRouter()


@router.post(
    "/users/{user_id}/tasks",
    status_code=201,
    response_model=TaskResponse,
    responses={
        201: {"description": "Task created successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied"},
        422: {"description": "Validation error"},
    },
)
async def create_task(
    user_id: uuid.UUID,
    data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    verify_user_ownership(user_id, current_user)

    task = Task(
        title=data.title.strip(),
        description=data.description,
        user_id=current_user.id,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.get(
    "/users/{user_id}/tasks",
    response_model=TaskListResponse,
    responses={
        200: {"description": "Task list retrieved"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied"},
    },
)
async def list_tasks(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=50, le=100, ge=1),
    offset: int = Query(default=0, ge=0),
):
    verify_user_ownership(user_id, current_user)

    count_result = await db.execute(
        select(func.count()).select_from(Task).where(Task.user_id == current_user.id)
    )
    total = count_result.scalar_one()

    result = await db.execute(
        select(Task)
        .where(Task.user_id == current_user.id)
        .order_by(col(Task.created_at).desc())
        .limit(limit)
        .offset(offset)
    )
    tasks = result.scalars().all()

    return TaskListResponse(tasks=tasks, total=total)


@router.get(
    "/users/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    responses={
        200: {"description": "Task retrieved"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied"},
        404: {"description": "Task not found"},
    },
)
async def get_task(
    user_id: uuid.UUID,
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    verify_user_ownership(user_id, current_user)

    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalars().first()
    if not task:
        raise NotFoundError(message="Task not found")
    return task


@router.put(
    "/users/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    responses={
        200: {"description": "Task updated successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied"},
        404: {"description": "Task not found"},
        422: {"description": "Validation error"},
    },
)
async def update_task(
    user_id: uuid.UUID,
    task_id: uuid.UUID,
    data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    verify_user_ownership(user_id, current_user)

    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalars().first()
    if not task:
        raise NotFoundError(message="Task not found")

    if data.title is not None:
        task.title = data.title.strip()
    if data.description is not None:
        task.description = data.description

    task.updated_at = datetime.now(timezone.utc)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.delete(
    "/users/{user_id}/tasks/{task_id}",
    status_code=204,
    responses={
        204: {"description": "Task deleted successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied"},
        404: {"description": "Task not found"},
    },
)
async def delete_task(
    user_id: uuid.UUID,
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    verify_user_ownership(user_id, current_user)

    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalars().first()
    if not task:
        raise NotFoundError(message="Task not found")

    await db.delete(task)
    await db.commit()


@router.patch(
    "/users/{user_id}/tasks/{task_id}/complete",
    response_model=TaskResponse,
    responses={
        200: {"description": "Task completion toggled"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied"},
        404: {"description": "Task not found"},
    },
)
async def toggle_complete(
    user_id: uuid.UUID,
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    verify_user_ownership(user_id, current_user)

    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalars().first()
    if not task:
        raise NotFoundError(message="Task not found")

    task.is_completed = not task.is_completed
    task.updated_at = datetime.now(timezone.utc)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task
