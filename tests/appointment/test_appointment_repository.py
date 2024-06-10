from datetime import datetime, timezone

from util_functions import get_random_user

from app.models import Appointment
from app.repositories.appointment_repository import AppointmentRepository
from app.services.user_service import UserService


async def test_appointment_repository_save(async_session):
    repo = AppointmentRepository(async_session)
    service = UserService(async_session)

    doctor = get_random_user(doctor=True)
    db_doctor = await service.create_user(doctor)
    patient = get_random_user(patient=True)
    db_patient = await service.create_user(patient)

    appointment = Appointment(
        doctor_id=db_doctor.doctor.id,
        patient_id=db_patient.patient.id,
        reason='test',
        notes='test notes',
        date=datetime.now(timezone.utc),
    )

    db_appointment = await repo.save(appointment)

    assert db_appointment
    assert db_appointment.id is not None
    assert db_appointment.reason == 'test'
    assert db_appointment.notes == 'test notes'


async def test_appointment_repository_get_by_id(async_session):
    repo = AppointmentRepository(async_session)
    service = UserService(async_session)

    doctor = get_random_user(doctor=True)
    db_doctor = await service.create_user(doctor)
    patient = get_random_user(patient=True)
    db_patient = await service.create_user(patient)

    appointment = Appointment(
        doctor_id=db_doctor.doctor.id,
        patient_id=db_patient.patient.id,
        reason='test',
        notes='test notes',
        date=datetime.now(timezone.utc),
    )

    db_appointment = await repo.save(appointment)
    fetched_appointment = await repo.get_by_id(db_appointment.id)

    assert fetched_appointment
    assert fetched_appointment.id == db_appointment.id
    assert fetched_appointment.reason == 'test'
    assert fetched_appointment.notes == 'test notes'


async def test_appointment_repository_get_all(async_session):
    repo = AppointmentRepository(async_session)
    service = UserService(async_session)

    doctor = get_random_user(doctor=True)
    db_doctor = await service.create_user(doctor)
    patient = get_random_user(patient=True)
    db_patient = await service.create_user(patient)

    appointment1 = Appointment(
        doctor_id=db_doctor.doctor.id,
        patient_id=db_patient.patient.id,
        reason='test1',
        notes='test notes 1',
        date=datetime.now(timezone.utc),
    )
    appointment2 = Appointment(
        doctor_id=db_doctor.doctor.id,
        patient_id=db_patient.patient.id,
        reason='test2',
        notes='test notes 2',
        date=datetime.now(timezone.utc),
    )

    await repo.save(appointment1)
    await repo.save(appointment2)

    all_appointments = await repo.get_all()

    assert len(all_appointments) == 2
    assert any(app.reason == 'test1' for app in all_appointments)
    assert any(app.reason == 'test2' for app in all_appointments)


async def test_appointment_repository_update(async_session):
    repo = AppointmentRepository(async_session)
    service = UserService(async_session)

    doctor = get_random_user(doctor=True)
    db_doctor = await service.create_user(doctor)
    patient = get_random_user(patient=True)
    db_patient = await service.create_user(patient)

    appointment = Appointment(
        doctor_id=db_doctor.doctor.id,
        patient_id=db_patient.patient.id,
        reason='test',
        notes='test notes',
        date=datetime.now(timezone.utc),
    )

    db_appointment = await repo.save(appointment)
    db_appointment.notes = 'updated notes'
    await repo.update(db_appointment, db_appointment)

    updated_appointment = await repo.get_by_id(db_appointment.id)

    assert updated_appointment
    assert updated_appointment.notes == 'updated notes'


async def test_appointment_repository_delete(async_session):
    repo = AppointmentRepository(async_session)
    service = UserService(async_session)

    doctor = get_random_user(doctor=True)
    db_doctor = await service.create_user(doctor)
    patient = get_random_user(patient=True)
    db_patient = await service.create_user(patient)

    appointment = Appointment(
        doctor_id=db_doctor.doctor.id,
        patient_id=db_patient.patient.id,
        reason='test',
        notes='test notes',
        date=datetime.now(timezone.utc),
    )

    db_appointment = await repo.save(appointment)
    await repo.delete_by_id(db_appointment.id)

    deleted_appointment = await repo.get_by_id(db_appointment.id)

    assert deleted_appointment is None


async def test_appointment_relationships(async_session):
    repo = AppointmentRepository(async_session)
    service = UserService(async_session)

    doctor = get_random_user(doctor=True)
    db_doctor = await service.create_user(doctor)
    patient = get_random_user(patient=True)
    db_patient = await service.create_user(patient)

    appointment = Appointment(
        doctor_id=db_doctor.doctor.id,
        patient_id=db_patient.patient.id,
        reason='checkup',
        notes='annual checkup',
        date=datetime.now(timezone.utc),
    )

    db_appointment = await repo.save(appointment)

    # assert db_appointment
    assert db_appointment.doctor_id == db_doctor.doctor.id
    assert db_appointment.patient_id == db_patient.patient.id

    # Verificar relacionamentos reversos
    assert db_appointment.doctor
    assert db_appointment.doctor.id == db_doctor.doctor.id
    assert db_appointment.patient
    assert db_appointment.patient.id == db_patient.patient.id

    assert await db_appointment.doctor.get_appointments()
    assert await db_appointment.patient.get_appointments()


async def test_doctor_appointments_relationship(async_session):
    repo = AppointmentRepository(async_session)
    service = UserService(async_session)

    doctor = get_random_user(doctor=True)
    db_doctor = await service.create_user(doctor)
    patient = get_random_user(patient=True)
    db_patient = await service.create_user(patient)

    appointment = Appointment(
        doctor_id=db_doctor.doctor.id,
        patient_id=db_patient.patient.id,
        reason='checkup',
        notes='annual checkup',
        date=datetime.now(timezone.utc),
    )

    db_appointment = await repo.save(appointment)

    # Fetch doctor with appointments
    doctor_appointments = await db_doctor.doctor.get_appointments()

    assert doctor_appointments
    assert len(doctor_appointments) == 1
    assert doctor_appointments[0].id == db_appointment.id


async def test_patient_appointments_relationship(async_session):
    repo = AppointmentRepository(async_session)
    service = UserService(async_session)

    doctor = get_random_user(doctor=True)
    db_doctor = await service.create_user(doctor)
    patient = get_random_user(patient=True)
    db_patient = await service.create_user(patient)

    appointment = Appointment(
        doctor_id=db_doctor.doctor.id,
        patient_id=db_patient.patient.id,
        reason='checkup',
        notes='annual checkup',
        date=datetime.now(timezone.utc),
    )

    db_appointment = await repo.save(appointment)

    # Fetch patient with appointments
    patient_appointments = await db_patient.patient.get_appointments()

    assert patient_appointments
    assert len(patient_appointments) == 1
    assert patient_appointments[0].id == db_appointment.id
