import random
import string
from datetime import datetime, timezone
from uuid import uuid1

from app.schemas.user_schemas import UserCreateRequest
from app.types.user import UserGender, UserType


def get_random_user_type(doctor, patient) -> dict:
    rand_num = random.randint(0, 1)

    if patient:
        rand_num = 0
    elif doctor:
        rand_num = 1

    if rand_num == 0:
        return dict(
            cpf=''.join([str(random.randint(0, 9)) for _ in range(11)]),
            sus_card=''.join([str(random.randint(0, 9)) for _ in range(15)]),
        )
    elif rand_num == 1:
        crm1 = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        crm2 = ''.join([str(random.randint(0, 9)) for _ in range(2)])
        crm = crm1 + '-' + crm2 + '/' + ''.join([random.choice(string.ascii_letters.upper()) for _ in range(2)])
        return dict(
            crm=crm,
            specialty=''.join([random.choice(string.ascii_letters) for _ in range(10)]),
        )


def get_random_user(
    additional_fields: dict = {}, /, request=False, doctor=False, patient=False
) -> UserCreateRequest | dict:

    # Generate random fields
    random_name = ' '.join([''.join([random.choice(string.ascii_letters) for _ in range(5)]) for _ in range(3)])
    user_type = random.choice([UserType.patient, UserType.doctor, UserType.admin])
    random_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    random_gender = random.choice([UserGender.male, UserGender.female, UserGender.other])
    random_email = uuid1().hex + '@email.com'

    user_data = dict(
        user=dict(
            name=random_name,
            email=random_email,
            gender=random_gender.value,
            phone=f'+55119{random_number}',
            user_type=user_type.value,
            password='DummyPassword321!',
            birthdate=datetime.now(timezone.utc).isoformat(),
        )
    )

    user_type = get_random_user_type(doctor, patient)

    if 'cpf' in user_type:
        user_data['user']['user_type'] = 'patient'
        user_data['patient'] = user_type
    elif 'crm' in user_type:
        user_data['user']['user_type'] = 'doctor'
        user_data['doctor'] = user_type

    # Update with additional fields if needed
    user_data['user'].update(additional_fields)

    if request:
        return user_data

    return UserCreateRequest(**user_data)
