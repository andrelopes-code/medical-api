from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, engine_from_config, pool

from app.core import settings
from app.models import SQLModel

sync_uri = settings.databases.postgres_uri.replace('+asyncpg', '')

database_urls = {
    'db1': sync_uri,
    'db2': sync_uri + '_test',
}

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline(db_uri) -> None:

    context.configure(
        url=db_uri,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(db_uri) -> None:

    connectable = create_engine(db_uri)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    for db_uri in database_urls.values():
        run_migrations_offline(db_uri)
else:
    for db_uri in database_urls.values():
        run_migrations_online(db_uri)
