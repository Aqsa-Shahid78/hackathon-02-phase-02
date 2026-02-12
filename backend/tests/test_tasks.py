import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Task
from app.security import create_access_token
from tests.conftest import auth_cookies


# --- Helper ---

async def create_task_for_user(db: AsyncSession, user: User, title: str = "Test Task") -> Task:
    task = Task(
        id=uuid.uuid4(),
        title=title,
        description="A test task description",
        user_id=user.id,
    )
    db.add(task)
    await db.flush()
    return task


# ========================
# T063: Task CRUD Tests
# ========================

class TestCreateTask:
    async def test_create_task_success(self, authed_client: AsyncClient, test_user: User):
        response = await authed_client.post(
            f"/api/v1/users/{test_user.id}/tasks",
            json={"title": "My new task", "description": "Some details"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "My new task"
        assert data["description"] == "Some details"
        assert data["is_completed"] is False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_create_task_title_only(self, authed_client: AsyncClient, test_user: User):
        response = await authed_client.post(
            f"/api/v1/users/{test_user.id}/tasks",
            json={"title": "Title only task"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Title only task"
        assert data["description"] is None

    async def test_create_task_empty_title(self, authed_client: AsyncClient, test_user: User):
        response = await authed_client.post(
            f"/api/v1/users/{test_user.id}/tasks",
            json={"title": "", "description": "desc"},
        )
        assert response.status_code == 422

    async def test_create_task_title_too_long(self, authed_client: AsyncClient, test_user: User):
        response = await authed_client.post(
            f"/api/v1/users/{test_user.id}/tasks",
            json={"title": "x" * 256},
        )
        assert response.status_code == 422

    async def test_create_task_description_too_long(self, authed_client: AsyncClient, test_user: User):
        response = await authed_client.post(
            f"/api/v1/users/{test_user.id}/tasks",
            json={"title": "Valid", "description": "x" * 2001},
        )
        assert response.status_code == 422

    async def test_create_task_unauthenticated(self, client: AsyncClient, test_user: User):
        response = await client.post(
            f"/api/v1/users/{test_user.id}/tasks",
            json={"title": "Should fail"},
        )
        assert response.status_code == 401


class TestListTasks:
    async def test_list_tasks_empty(self, authed_client: AsyncClient, test_user: User):
        response = await authed_client.get(f"/api/v1/users/{test_user.id}/tasks")
        assert response.status_code == 200
        data = response.json()
        assert data["tasks"] == []
        assert data["total"] == 0

    async def test_list_tasks_with_data(
        self, authed_client: AsyncClient, test_user: User, db_session: AsyncSession
    ):
        await create_task_for_user(db_session, test_user, "Task 1")
        await create_task_for_user(db_session, test_user, "Task 2")

        response = await authed_client.get(f"/api/v1/users/{test_user.id}/tasks")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["tasks"]) == 2

    async def test_list_tasks_pagination(
        self, authed_client: AsyncClient, test_user: User, db_session: AsyncSession
    ):
        for i in range(5):
            await create_task_for_user(db_session, test_user, f"Task {i}")

        response = await authed_client.get(
            f"/api/v1/users/{test_user.id}/tasks?limit=2&offset=0"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert len(data["tasks"]) == 2

    async def test_list_tasks_unauthenticated(self, client: AsyncClient, test_user: User):
        response = await client.get(f"/api/v1/users/{test_user.id}/tasks")
        assert response.status_code == 401


class TestGetTask:
    async def test_get_task_success(
        self, authed_client: AsyncClient, test_user: User, db_session: AsyncSession
    ):
        task = await create_task_for_user(db_session, test_user)
        response = await authed_client.get(
            f"/api/v1/users/{test_user.id}/tasks/{task.id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Task"

    async def test_get_task_not_found(self, authed_client: AsyncClient, test_user: User):
        fake_id = uuid.uuid4()
        response = await authed_client.get(
            f"/api/v1/users/{test_user.id}/tasks/{fake_id}"
        )
        assert response.status_code == 404
        data = response.json()
        assert data["error"]["code"] == "NOT_FOUND"


class TestUpdateTask:
    async def test_update_task_success(
        self, authed_client: AsyncClient, test_user: User, db_session: AsyncSession
    ):
        task = await create_task_for_user(db_session, test_user)
        response = await authed_client.put(
            f"/api/v1/users/{test_user.id}/tasks/{task.id}",
            json={"title": "Updated Title", "description": "Updated desc"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated desc"

    async def test_update_task_partial(
        self, authed_client: AsyncClient, test_user: User, db_session: AsyncSession
    ):
        task = await create_task_for_user(db_session, test_user)
        response = await authed_client.put(
            f"/api/v1/users/{test_user.id}/tasks/{task.id}",
            json={"title": "New Title Only"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title Only"

    async def test_update_task_not_found(self, authed_client: AsyncClient, test_user: User):
        fake_id = uuid.uuid4()
        response = await authed_client.put(
            f"/api/v1/users/{test_user.id}/tasks/{fake_id}",
            json={"title": "No task"},
        )
        assert response.status_code == 404

    async def test_update_task_validation_error(
        self, authed_client: AsyncClient, test_user: User, db_session: AsyncSession
    ):
        task = await create_task_for_user(db_session, test_user)
        response = await authed_client.put(
            f"/api/v1/users/{test_user.id}/tasks/{task.id}",
            json={"title": "x" * 256},
        )
        assert response.status_code == 422


class TestDeleteTask:
    async def test_delete_task_success(
        self, authed_client: AsyncClient, test_user: User, db_session: AsyncSession
    ):
        task = await create_task_for_user(db_session, test_user)
        response = await authed_client.delete(
            f"/api/v1/users/{test_user.id}/tasks/{task.id}"
        )
        assert response.status_code == 204

    async def test_delete_task_not_found(self, authed_client: AsyncClient, test_user: User):
        fake_id = uuid.uuid4()
        response = await authed_client.delete(
            f"/api/v1/users/{test_user.id}/tasks/{fake_id}"
        )
        assert response.status_code == 404


class TestToggleComplete:
    async def test_toggle_complete_success(
        self, authed_client: AsyncClient, test_user: User, db_session: AsyncSession
    ):
        task = await create_task_for_user(db_session, test_user)
        assert task.is_completed is False

        response = await authed_client.patch(
            f"/api/v1/users/{test_user.id}/tasks/{task.id}/complete"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_completed"] is True

    async def test_toggle_complete_back(
        self, authed_client: AsyncClient, test_user: User, db_session: AsyncSession
    ):
        task = await create_task_for_user(db_session, test_user)

        # Toggle to True
        await authed_client.patch(
            f"/api/v1/users/{test_user.id}/tasks/{task.id}/complete"
        )
        # Toggle back to False
        response = await authed_client.patch(
            f"/api/v1/users/{test_user.id}/tasks/{task.id}/complete"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_completed"] is False

    async def test_toggle_not_found(self, authed_client: AsyncClient, test_user: User):
        fake_id = uuid.uuid4()
        response = await authed_client.patch(
            f"/api/v1/users/{test_user.id}/tasks/{fake_id}/complete"
        )
        assert response.status_code == 404


# ==============================
# T064: Data Isolation Tests
# ==============================

class TestDataIsolation:
    """User A must NOT be able to access User B's tasks."""

    async def test_user_cannot_list_other_users_tasks(
        self, client: AsyncClient, test_user: User, second_user: User, db_session: AsyncSession
    ):
        await create_task_for_user(db_session, second_user, "Secret task")

        # Authenticate as test_user, try to list second_user's tasks
        token = create_access_token(subject=str(test_user.id))
        client.cookies.set("access_token", token)

        response = await client.get(f"/api/v1/users/{second_user.id}/tasks")
        assert response.status_code == 403

    async def test_user_cannot_get_other_users_task(
        self, client: AsyncClient, test_user: User, second_user: User, db_session: AsyncSession
    ):
        task = await create_task_for_user(db_session, second_user, "Secret task")

        token = create_access_token(subject=str(test_user.id))
        client.cookies.set("access_token", token)

        response = await client.get(f"/api/v1/users/{second_user.id}/tasks/{task.id}")
        assert response.status_code == 403

    async def test_user_cannot_update_other_users_task(
        self, client: AsyncClient, test_user: User, second_user: User, db_session: AsyncSession
    ):
        task = await create_task_for_user(db_session, second_user, "Secret task")

        token = create_access_token(subject=str(test_user.id))
        client.cookies.set("access_token", token)

        response = await client.put(
            f"/api/v1/users/{second_user.id}/tasks/{task.id}",
            json={"title": "Hacked"},
        )
        assert response.status_code == 403

    async def test_user_cannot_delete_other_users_task(
        self, client: AsyncClient, test_user: User, second_user: User, db_session: AsyncSession
    ):
        task = await create_task_for_user(db_session, second_user, "Secret task")

        token = create_access_token(subject=str(test_user.id))
        client.cookies.set("access_token", token)

        response = await client.delete(f"/api/v1/users/{second_user.id}/tasks/{task.id}")
        assert response.status_code == 403

    async def test_user_cannot_toggle_other_users_task(
        self, client: AsyncClient, test_user: User, second_user: User, db_session: AsyncSession
    ):
        task = await create_task_for_user(db_session, second_user, "Secret task")

        token = create_access_token(subject=str(test_user.id))
        client.cookies.set("access_token", token)

        response = await client.patch(
            f"/api/v1/users/{second_user.id}/tasks/{task.id}/complete"
        )
        assert response.status_code == 403

    async def test_user_id_path_mismatch(
        self, authed_client: AsyncClient, test_user: User
    ):
        """User's JWT is valid but path user_id doesn't match → 403."""
        other_user_id = uuid.uuid4()
        response = await authed_client.get(f"/api/v1/users/{other_user_id}/tasks")
        assert response.status_code == 403
        data = response.json()
        assert data["error"]["code"] == "FORBIDDEN"


# ==============================
# T065: Error Response Format
# ==============================

class TestErrorResponseFormat:
    """All errors must return {error: {code, message, details}}."""

    async def test_401_format(self, client: AsyncClient, test_user: User):
        response = await client.post(
            "/api/v1/auth/signin",
            json={"email": "nobody@example.com", "password": "wrong"},
        )
        assert response.status_code == 401
        data = response.json()
        assert "error" in data
        assert "code" in data["error"]
        assert "message" in data["error"]
        assert "details" in data["error"]

    async def test_403_format(self, authed_client: AsyncClient, test_user: User):
        other_id = uuid.uuid4()
        response = await authed_client.get(f"/api/v1/users/{other_id}/tasks")
        assert response.status_code == 403
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "FORBIDDEN"
        assert "message" in data["error"]
        assert "details" in data["error"]

    async def test_404_format(self, authed_client: AsyncClient, test_user: User):
        fake_id = uuid.uuid4()
        response = await authed_client.get(
            f"/api/v1/users/{test_user.id}/tasks/{fake_id}"
        )
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "NOT_FOUND"
        assert "message" in data["error"]

    async def test_409_format(self, client: AsyncClient, test_user: User):
        response = await client.post(
            "/api/v1/auth/signup",
            json={"email": test_user.email, "password": "securepass123"},
        )
        assert response.status_code == 409
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "CONFLICT"
        assert "message" in data["error"]
