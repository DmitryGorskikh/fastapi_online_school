import pytest
from sqlalchemy import select

from app.infrastructure.database.models import (
    TaskAttemptModel
)
import app.presentation.api.dependencies as api_dependencies


class FakeSubmissionQueue:
    def __init__(self) -> None:
        self.items = []

    async def enqueue(self, submission_id) -> None:
        self.items.append(submission_id)


@pytest.fixture
def fake_submission_queue(monkeypatch):
    queue = FakeSubmissionQueue()
    monkeypatch.setattr(
        api_dependencies,
        'build_submission_queue',
        lambda: queue,
    )
    return queue


@pytest.mark.asyncio
async def test_task_flow_create_and_delete(
    client, author_auth_headers, seeded_tasks_tree
):
    headers = author_auth_headers
    tree = seeded_tasks_tree

    delete_task = await client.delete(
        f'/api/admin/tasks/{tree.task_id}', headers=headers,
    )
    assert delete_task.status_code == 204

    structure = await client.get(f'/api/courses/{tree.course_id}/structure')
    section = structure.json()['modules'][0]['sections'][0]
    assert tree.task_id not in section['task_ids']


@pytest.mark.asyncio
async def test_task_delete_blocked_after_attempt(
    client, author_auth_headers, student_auth_headers, seeded_tasks_tree,
    session_factory,
):
    tree = seeded_tasks_tree
    attempt = await client.post(
        f'/api/learning/tasks/{tree.task_id}/attempts',
        headers=student_auth_headers,
        json={'submitted_answer': 'GET'},
    )
    assert attempt.status_code == 201

    delete_task = await client.delete(
        f'/api/admin/tasks/{tree.task_id}', headers=author_auth_headers,
    )
    assert delete_task.status_code == 400

    structure = await client.get(f'/api/courses/{tree.course_id}/structure')
    section = structure.json()['modules'][0]['sections'][0]
    assert tree.task_id in section['task_ids']

    async with session_factory() as session:
        result = await session.execute(
            select(TaskAttemptModel).where(
                TaskAttemptModel.task_id == tree.task_id
            )
        )
        assert len(result.scalars().all()) == 1


@pytest.mark.asyncio
async def test_test_case_flow(
    client, author_auth_headers, student_auth_headers, seeded_tasks_tree,
    fake_submission_queue
):
    headers = author_auth_headers
    tree = seeded_tasks_tree

    test_case_1 = (await client.post(
        f'/api/admin/code-tasks/{tree.code_task_id}/test-cases',
        headers=headers,
        json={'position': 1, 'input_data': '1 2', 'expected_output': '3',
              'is_hidden': False, 'explanation': ''},
    )).json()['id']
    test_case_2 = (await client.post(
        f'/api/admin/code-tasks/{tree.code_task_id}/test-cases',
        headers=headers,
        json={'position': 2, 'input_data': '5 5', 'expected_output': '10',
              'is_hidden': False, 'explanation': ''},
    )).json()['id']

    assert test_case_1
    assert test_case_2

    submit = await client.post(
        f'/api/learning/code-tasks/{tree.code_task_id}/submissions',
        headers=student_auth_headers,
        json={'source_code': 'print(sum(map(int, input().split())))'},
    )
    assert submit.status_code == 202

    delete_after_submission = await client.delete(
        f'/api/admin/test-cases/{test_case_2}', headers=headers
    )
    assert delete_after_submission.status_code == 400
