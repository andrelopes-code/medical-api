import random
import string
from datetime import datetime
from uuid import uuid1

from app.models import User


def get_random_user() -> User:

    random_name = ' '.join([''.join([random.choice(string.ascii_letters) for _ in range(5)]) for _ in range(3)])
    user_type = random.choice(['patient', 'doctor', 'admin'])
    random_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    random_gender = random.choice(['male', 'female', 'other'])
    random_email = uuid1().hex + '@email.com'
    return User(
        name=random_name,
        email=random_email,
        gender=random_gender,
        phone=f'+55119{random_number}',
        user_type=user_type,
        password='DummyPassword321!',
        birthdate=datetime.now(),
    )
