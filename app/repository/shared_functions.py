import asyncio
from app.core import logger


def update_model_fields(model, data):
    """Updates the given model fields with the given data"""
    if isinstance(data, dict):
        for field, value in data.items():
            if value is not None:
                setattr(model, field, value)
    else:
        for field, value in data:
            if value is not None:
                setattr(model, field, value)


def sqlalchemy_exception_handler(method):

    async def async_wrapper(self, *args, **kwargs):
        try:
            return await method(self, *args, **kwargs)
        except Exception as e:
            logger.error(f'Error executing method [[bold red]{method.__name__}[/bold red]]: {e}')

    def sync_wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception as e:
            logger.error(f'Error executing method [[bold red]{method.__name__}[/bold red]]: {e}')

    # Detecta se o método é uma coroutine
    if asyncio.iscoroutinefunction(method):
        return async_wrapper
    else:
        return sync_wrapper


def handle_sqlalchemy_exception(cls):
    for name in dir(cls):
        if not name.startswith('__'):
            method = getattr(cls, name)
            if callable(method):
                setattr(cls, name, sqlalchemy_exception_handler(method))
    return cls
