from datetime import datetime, timezone
import typer
import asyncio
import inspect
from functools import wraps

from app.core.security.auth import AuthService
from app.models.user import User
from app.schemas.user_schemas import UserCreate
from app.repositories.user_repository import UserRepository
from app.types.user import UserGender, UserType
from app.core.databases.postgres import sessionmaker


class ATyper(typer.Typer):
    def command(self, *args, **kwargs):
        decorator = super().command(*args, **kwargs)

        def add_runner(f):

            @wraps(f)
            def runner(*args, **kwargs):
                asyncio.run(f(*args, **kwargs))

            if inspect.iscoroutinefunction(f):
                return decorator(runner)
            return decorator(f)

        return add_runner


app = ATyper(name='Medical Appointments', add_completion=False)


@app.command()
async def create_admin(email: str, password: str, name: str):
    async with sessionmaker() as session:
        repository = UserRepository(session)

        user = User.model_validate(
            UserCreate(
                email=email,
                password=password,
                user_type=UserType.admin,
                birthdate=datetime.now(timezone.utc).isoformat(),
                gender=UserGender.male,
                name='Admin User',
                phone='+5511999999999',
            )
        )

        await repository.save(user)

        print('User created successfully!')


@app.command()
async def login(email: str, password: str):
    auth_service = AuthService()
    try:
        access_token = await auth_service.login_user(email=email, password=password)
    except Exception as e:
        print(e)
        return

    print('Access Token: ', access_token['access_token'])
