from datetime import datetime, timedelta, timezone

from httpx import AsyncClient
from util_functions import get_random_user


async def test_create_user(async_client: AsyncClient, json_headers, async_session):

    user = get_random_user(request=True, doctor=True)
    response = await async_client.post('/user', headers=json_headers, json=user)
    doctor_user = response.json()
    user = get_random_user(request=True, patient=True)
    response = await async_client.post('/user', headers=json_headers, json=user)
    patient_user = response.json()

    appo = dict(
        date=(datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        reason='test',
        notes='test',
        doctor_id=doctor_user['doctor']['id'],
        patient_id=patient_user['patient']['id'],
    )

    response = await async_client.post('/appointment', headers=json_headers, json=appo)
    assert response.status_code == 201


async def test_get_all_appointments(async_client: AsyncClient, json_headers, async_session):

    user = get_random_user(request=True, doctor=True)
    response = await async_client.post('/user', headers=json_headers, json=user)
    doctor_user = response.json()
    user = get_random_user(request=True, patient=True)
    response = await async_client.post('/user', headers=json_headers, json=user)
    patient_user = response.json()

    appo = dict(
        date=(datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        reason='test',
        notes='test',
        doctor_id=doctor_user['doctor']['id'],
        patient_id=patient_user['patient']['id'],
    )

    create_response = await async_client.post('/appointment', headers=json_headers, json=appo)
    assert create_response.status_code == 201

    response = await async_client.get('/appointment', headers=json_headers)
    assert response.status_code == 200
    assert response.json() == [create_response.json()]


async def test_update_appointment(async_client: AsyncClient, json_headers, async_session):

    user = get_random_user(request=True, doctor=True)
    response = await async_client.post('/user', headers=json_headers, json=user)
    doctor_user = response.json()
    user = get_random_user(request=True, patient=True)
    response = await async_client.post('/user', headers=json_headers, json=user)
    patient_user = response.json()

    appo = dict(
        date=(datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        reason='test',
        notes='test',
        doctor_id=doctor_user['doctor']['id'],
        patient_id=patient_user['patient']['id'],
    )

    create_response = await async_client.post('/appointment', headers=json_headers, json=appo)
    assert create_response.status_code == 201

    update_data = dict(
        date=(datetime.now(timezone.utc) + timedelta(days=2)).isoformat(),
        reason='test update',
        notes='test update',
    )

    response = await async_client.patch(
        f'/appointment/{create_response.json()["id"]}', headers=json_headers, json=update_data
    )
    assert response.status_code == 200
    assert response.json()['reason'] == update_data['reason']

    new_response = await async_client.get('/appointment', headers=json_headers)
    assert new_response.status_code == 200
    assert new_response.json()[0]['reason'] == update_data['reason']


async def test_delete_appointment(async_client: AsyncClient, json_headers, async_session):

    user = get_random_user(request=True, doctor=True)
    response = await async_client.post('/user', headers=json_headers, json=user)
    doctor_user = response.json()
    user = get_random_user(request=True, patient=True)
    response = await async_client.post('/user', headers=json_headers, json=user)
    patient_user = response.json()

    appo = dict(
        date=(datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        reason='test',
        notes='test',
        doctor_id=doctor_user['doctor']['id'],
        patient_id=patient_user['patient']['id'],
    )

    create_response = await async_client.post('/appointment', headers=json_headers, json=appo)
    assert create_response.status_code == 201

    response = await async_client.delete(f'/appointment/{create_response.json()["id"]}', headers=json_headers)
    assert response.status_code == 200
    assert response.json()['is_deleted'] is True

    new_response = await async_client.get('/appointment', headers=json_headers)
    assert new_response.status_code == 200
    assert new_response.json() == []


async def test_get_user_appointments(async_client: AsyncClient, json_headers, async_session):

    user = get_random_user(request=True, doctor=True)
    response = await async_client.post('/user', headers=json_headers, json=user)
    doctor_user = response.json()
    user = get_random_user(request=True, patient=True)
    response = await async_client.post('/user', headers=json_headers, json=user)
    patient_user = response.json()

    appo = dict(
        date=(datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        reason='test',
        notes='test',
        doctor_id=doctor_user['doctor']['id'],
        patient_id=patient_user['patient']['id'],
    )

    create_response = await async_client.post('/appointment', headers=json_headers, json=appo)
    assert create_response.status_code == 201

    response = await async_client.get(f'/appointment/user/{patient_user["id"]}', headers=json_headers)
    assert response.status_code == 200
    assert response.json() == [create_response.json()]
