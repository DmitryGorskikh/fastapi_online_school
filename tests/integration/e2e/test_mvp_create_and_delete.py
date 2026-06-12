import pytest


@pytest.mark.asyncio
async def test_mvp_flow_to_delete(
    client, admin_auth_headers
):
    headers = admin_auth_headers

    course_id = (await client.post(
        '/api/admin/courses',
        headers=headers,
        json={
            'title': 'FastAPI course',
            'description': 'Clean architecture.'
        },
    )
    ).json()['id']

    module_id = (await client.post(
        f'/api/admin/courses/{course_id}/modules',
        headers=headers,
        json={
            'title': 'MVP',
            'description': 'Content.', 'position': 1
        },
    )
    ).json()['id']

    section_id = (await client.post(
        f'/api/admin/modules/{module_id}/sections',
        headers=headers,
        json={
            'title': 'Auth',
            'description': 'JWT.', 'position': 1
        },
    )
    ).json()['id']

    lecture_id = (await client.post(
        f'/api/admin/sections/{section_id}/lectures',
        headers=headers,
        json={
            'title': 'Bearer',
            'content': 'Lecture content', 'position': 1
        },
    )
    ).json()['id']

    structure = await client.get(f'/api/courses/{course_id}/structure')
    assert len(structure.json()['modules']) == 1

    delete_response = await client.delete(
        f'/api/admin/modules/{module_id}',
        headers=headers,
    )
    assert delete_response.status_code == 204

    structure_after = await client.get(f'/api/courses/{course_id}/structure')
    assert structure_after.status_code == 200
    assert len(structure_after.json()['modules']) == 0

    lecture_read = await client.get(f'/api/lectures/{lecture_id}')
    assert lecture_read.status_code == 404

    course_read = await client.get(f'/api/courses/{course_id}')
    assert course_read.status_code == 200
