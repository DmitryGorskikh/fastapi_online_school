from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_delete_lecture_removes_it(
    client, admin_auth_headers, seeded_course_tree
):
    response = await client.delete(
        f'/api/admin/lectures/{seeded_course_tree.lecture_id}',
        headers=admin_auth_headers,
    )
    assert response.status_code == 204

    read = await client.get(f'/api/lectures/{seeded_course_tree.lecture_id}')
    assert read.status_code == 404

    structure = await client.get(
        f'/api/courses/{seeded_course_tree.course_id}/structure'
    )
    lectures = structure.json()['modules'][0]['sections'][0]['lectures']
    assert len(lectures) == 0


@pytest.mark.asyncio
async def test_delete_missing_lecture_returns_404(
    client, admin_auth_headers
):
    response = await client.delete(
        f'/api/admin/lectures/{uuid4()}',
        headers=admin_auth_headers,
    )
    assert response.status_code == 404
    assert response.json()['error'] == 'lecture_not_found'


@pytest.mark.asyncio
async def test_delete_section_cascades_to_lectures(
    client, admin_auth_headers, seeded_course_tree
):
    response = await client.delete(
        f'/api/admin/sections/{seeded_course_tree.section_id}',
        headers=admin_auth_headers,
    )
    assert response.status_code == 204

    lecture = await client.get(
        f'/api/lectures/{seeded_course_tree.lecture_id}'
    )
    assert lecture.status_code == 404

    structure = await client.get(
        f'/api/courses/{seeded_course_tree.course_id}/structure'
    )
    sections = structure.json()['modules'][0]['sections']
    assert len(sections) == 0


@pytest.mark.asyncio
async def test_delete_missing_section_returns_404(
    client, admin_auth_headers
):
    response = await client.delete(
        f'/api/admin/sections/{uuid4()}',
        headers=admin_auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_module_cascades(
    client, admin_auth_headers, seeded_course_tree
):
    response = await client.delete(
        f'/api/admin/modules/{seeded_course_tree.module_id}',
        headers=admin_auth_headers,
    )
    assert response.status_code == 204

    lecture = await client.get(
        f'/api/lectures/{seeded_course_tree.lecture_id}'
    )
    assert lecture.status_code == 404

    structure = await client.get(
        f'/api/courses/{seeded_course_tree.course_id}/structure'
    )
    assert len(structure.json()['modules']) == 0


@pytest.mark.asyncio
async def test_delete_missing_module_returns_404(
    client, admin_auth_headers
):
    response = await client.delete(
        f'/api/admin/modules/{uuid4()}',
        headers=admin_auth_headers,
    )
    assert response.status_code == 404


async def test_delete_course_cascades_everything(
    client, admin_auth_headers, seeded_course_tree
):
    response = await client.delete(
        f'/api/admin/courses/{seeded_course_tree.course_id}',
        headers=admin_auth_headers,
    )
    assert response.status_code == 204

    course = await client.get(
        f'/api/courses/{seeded_course_tree.course_id}'
    )
    assert course.status_code == 404

    courses = await client.get('/api/courses')
    assert courses.json() == []

    lecture = await client.get(
        f'/api/lectures/{seeded_course_tree.lecture_id}'
    )
    assert lecture.status_code == 404


@pytest.mark.asyncio
async def test_delete_missing_course_returns_404(
    client, admin_auth_headers
):
    response = await client.delete(
        f'/api/admin/courses/{uuid4()}',
        headers=admin_auth_headers,
    )
    assert response.status_code == 404
    assert response.json()['error'] == 'course_not_found'


@pytest.mark.asyncio
async def test_student_cannot_delete_lecture(
    client, student_auth_headers, seeded_course_tree
):
    response = await client.delete(
        f'/api/admin/lectures/{seeded_course_tree.lecture_id}',
        headers=student_auth_headers,
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_anonymous_cannot_delete_lecture(
    client, seeded_course_tree
):
    response = await client.delete(
        f'/api/admin/lectures/{seeded_course_tree.lecture_id}',
    )
    assert response.status_code == 401
