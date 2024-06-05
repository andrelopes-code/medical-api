import asyncio
import traceback

from sqlalchemy.exc import SQLAlchemyError

from app.core import logger
from app.core.exceptions import HttpExceptions


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


def exception_handler(
    method: callable, log_message: str, exception_to_raise: Exception, TargetException: Exception = Exception
):

    async def async_wrapper(self, *args, **kwargs):
        try:
            return await method(self, *args, **kwargs)
        except TargetException as e:
            self.session.rollback()
            exception_info = traceback.extract_tb(e.__traceback__)[-1]
            file = exception_info.filename
            line = exception_info.lineno
            module = exception_info.name
            logger.error(log_message, exc=e, class_and_method=f'{file}:{line}:{module}')
            raise exception_to_raise

    def sync_wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except TargetException as e:
            self.session.rollback()
            exception_info = traceback.extract_tb(e.__traceback__)[-1]
            file = exception_info.filename
            line = exception_info.lineno
            module = exception_info.name
            logger.error(log_message, exc=e, class_and_method=f'{file}:{line}:{module}')
            raise exception_to_raise

    return async_wrapper if asyncio.iscoroutinefunction(method) else sync_wrapper


def handle_sqlalchemy_exception(cls):
    """This decorator handles SQLAlchemyError exception, logs the error and raises HTTPException 500"""
    for method_name in dir(cls):
        if not method_name.startswith('_'):
            method = getattr(cls, method_name)
            if callable(method):
                log_message = 'Error while executing [ [bold blue]{class_and_method}[/bold blue] ]: {exc}'
                exception_to_raise = HttpExceptions.internal_server_error('An error occurred processing your request')

                setattr(
                    cls,
                    method_name,
                    exception_handler(
                        method=method,
                        log_message=log_message,
                        exception_to_raise=exception_to_raise,
                        TargetException=SQLAlchemyError,
                    ),
                )
    return cls
