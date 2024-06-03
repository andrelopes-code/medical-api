import os

from dynaconf import Dynaconf, Validator

HERE = os.path.dirname(os.path.abspath(__file__))

settings = Dynaconf(
    envvar_prefix='api',
    preload=[os.path.join(HERE, 'default.toml')],
    environments=['development', 'production', 'testing'],
    settings_files=['settings.toml', '.secrets.toml'],
    env_switcher='api_env',
    load_dotenv=False,
)

# Ensure that secret key is set
settings.validators.register(
    Validator('security.SECRET_KEY', must_exist=True)
)
settings.validators.validate()
