import random
import string
from datetime import datetime
from uuid import uuid1

from app.models import User
from app.types.user import UserGender, UserType


def get_random_user(additional_fields: dict = {}) -> User:

    # Generate random fields
    random_name = ' '.join([''.join([random.choice(string.ascii_letters) for _ in range(5)]) for _ in range(3)])
    user_type = random.choice([UserType.patient, UserType.doctor, UserType.admin])
    random_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    random_gender = random.choice([UserGender.male, UserGender.female, UserGender.other])
    random_email = uuid1().hex + '@email.com'

    user = dict(
        name=random_name,
        email=random_email,
        gender=random_gender,
        phone=f'+55119{random_number}',
        user_type=user_type,
        password='DummyPassword321!',
        birthdate=datetime.now(),
    )

    # Update with additional fields if needed
    user.update(additional_fields)

    return User(**user)
