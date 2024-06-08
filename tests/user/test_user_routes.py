from uuid import uuid4
from httpx import AsyncClient

from app.schemas.user_schemas import UserUpdateRequest
from util_functions import get_random_user


async def test_create_user(async_client: AsyncClient, json_headers, async_session):
    user = get_random_user(request=True)
    response = await async_client.post('/user', headers=json_headers, json=user)
    assert response.status_code == 201


async def test_get_users_empty(async_client: AsyncClient, authorization, async_session):
    response = await async_client.get('/user', headers=authorization)
    assert response.status_code == 200
    assert response.json() == []


async def test_create_and_get_users(async_client: AsyncClient, authorization, async_session):
    users = [get_random_user(request=True) for _ in range(10)]

    for user in users:
        response = await async_client.post('/user', headers=authorization, json=user)
        assert response.status_code == 201

    response = await async_client.get('/user', headers=authorization)
    assert response.status_code == 200
    assert len(response.json()) == len(users)


async def test_unauthorized_returns_401_and_header(async_client: AsyncClient, async_session):
    response = await async_client.get('/user')
    assert response.status_code == 401
    assert response.headers['WWW-Authenticate'] == 'Bearer'


async def test_get_user_by_id(async_client: AsyncClient, authorization, async_session):
    user = get_random_user(request=True)
    response = await async_client.post('/user', headers=authorization, json=user)
    assert response.status_code == 201

    response = await async_client.get(f'/user/{response.json()["id"]}', headers=authorization)
    assert response.status_code == 200
    assert response.json()['email'] == user['email']


async def test_get_inexistent_user(async_client: AsyncClient, authorization, async_session):
    response = await async_client.get(f'/user/{uuid4()}', headers=authorization)
    assert response.status_code == 404


async def test_update_user_by_id(async_client: AsyncClient, authorization, async_session):
    user = get_random_user(request=True)
    response = await async_client.post('/user', headers=authorization, json=user)
    assert response.status_code == 201

    update_data = UserUpdateRequest(**get_random_user(request=True)).model_dump()
    response = await async_client.patch(f'/user/{response.json()["id"]}', headers=authorization, json=update_data)
    assert response.status_code == 200
    assert response.json()['name'] == update_data['name']


async def test_update_inexistent_user(async_client: AsyncClient, authorization, async_session):
    update_data = UserUpdateRequest(**get_random_user(request=True)).model_dump()
    response = await async_client.patch(f'/user/{uuid4()}', headers=authorization, json=update_data)
    assert response.status_code == 404


async def test_invalid_create_user(async_client: AsyncClient, authorization, async_session):
    user = get_random_user(request=True)
    user['name'] = ''
    response = await async_client.post('/user', headers=authorization, json=user)
    assert response.status_code == 422


async def test_invalid_update_user(async_client: AsyncClient, authorization, async_session):
    user = get_random_user(request=True)
    response = await async_client.post('/user', headers=authorization, json=user)
    assert response.status_code == 201

    update_data = UserUpdateRequest(**get_random_user(request=True)).model_dump()
    update_data['name'] = ''
    response = await async_client.patch(f'/user/{response.json()["id"]}', headers=authorization, json=update_data)
    assert response.status_code == 422
