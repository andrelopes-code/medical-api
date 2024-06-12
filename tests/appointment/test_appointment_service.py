from app.services.appointment_service import AppointmentService
from app.schemas.appointment_schemas import AppointmentCreateRequest
from app.services.user_service import UserService
from datetime import datetime, timedelta, timezone
from util_functions import get_random_user


async def test_create_valid_appointment(async_session):
    appo_service = AppointmentService(async_session)
    user_service = UserService(async_session)

    doctor = get_random_user(doctor=True)
    db_doctor = await user_service.create_user(doctor)
    patient = get_random_user(patient=True)
    db_patient = await user_service.create_user(patient)

    appointment = AppointmentCreateRequest(
        doctor_id=db_doctor.doctor.id,
        patient_id=db_patient.patient.id,
        reason='test',
        notes='test notes',
        date=datetime.now(timezone.utc) + timedelta(minutes=61),
    )

    appo = await appo_service.create_appointment(appointment)

    assert appo
    assert appo.doctor_id == db_doctor.doctor.id
    assert appo.patient_id == db_patient.patient.id
    assert appo in await appo.doctor.get_appointments()


async def test_delete_appointment_and_get_appointment_by_id(async_session):
    appo_service = AppointmentService(async_session)
    user_service = UserService(async_session)

    doctor = get_random_user(doctor=True)
    db_doctor = await user_service.create_user(doctor)
    patient = get_random_user(patient=True)
    db_patient = await user_service.create_user(patient)

    appointment = AppointmentCreateRequest(
        doctor_id=db_doctor.doctor.id,
        patient_id=db_patient.patient.id,
        reason='test',
        notes='test notes',
        date=datetime.now(timezone.utc) + timedelta(minutes=61),
    )

    appo = await appo_service.create_appointment(appointment)

    deleted_appo = await appo_service.delete_appointment_by_id(appo.id)
    assert deleted_appo == appo
    none_appo = await appo_service.get_appointment_by_id(appo.id)
    assert none_appo is None


async def test_list_appointments(async_session):

    appo_service = AppointmentService(async_session)
    user_service = UserService(async_session)

    doctor = get_random_user(doctor=True)
    db_doctor = await user_service.create_user(doctor)
    patient = get_random_user(patient=True)
    db_patient = await user_service.create_user(patient)

    appointment1 = AppointmentCreateRequest(
        doctor_id=db_doctor.doctor.id,
        patient_id=db_patient.patient.id,
        reason='test1',
        notes='test notes',
        date=datetime.now(timezone.utc) + timedelta(minutes=61),
    )

    appointment2 = AppointmentCreateRequest(
        doctor_id=db_doctor.doctor.id,
        patient_id=db_patient.patient.id,
        reason='test2',
        notes='test notes',
        date=datetime.now(timezone.utc) + timedelta(minutes=61),
    )

    db_appo1 = await appo_service.create_appointment(appointment1)
    db_appo2 = await appo_service.create_appointment(appointment2)

    appointments = await appo_service.get_all_appointments()

    assert db_appo1 in appointments
    assert db_appo2 in appointments
