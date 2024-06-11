import asyncio
from typing import Callable, Tuple

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.core import logger
from app.core.exceptions import HttpExceptions


def __exception_handler(method: Callable, log_message: str, exception_to_raise: Exception, TargetExceptions=Exception):

    async def __async_wrapper(self, *args, **kwargs):
        try:
            return await method(self, *args, **kwargs)
        except TargetExceptions as e:
            if e.__class__ == HTTPException:
                raise
            try:
                await self.session.rollback()
            except Exception:
                pass
            logger.exception(log_message)
            raise exception_to_raise

    def __sync_wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except TargetExceptions as e:
            if e.__class__ == HTTPException:
                raise
            try:
                self.session.rollback()
            except Exception:
                pass
            logger.exception(log_message)
            raise exception_to_raise

    return __async_wrapper if asyncio.iscoroutinefunction(method) else __sync_wrapper


def handle_unexpected_exceptions(
    log_message: str | None = None,
    exceptions: Exception | Tuple[Exception] | None = None,
    exc_to_raise: Exception | None = None,
):
    """
    This decorator handles unexpected exceptions

    Usage:
    ```python
    @handle_unexpected_exceptions() # You have to use parentheses to call the decorator
    class SomeClass:

        # This method will be decorated
        def method(self):
            pass
    ```
    """

    log_message = log_message or 'Unexpected error occurred: '
    exc_to_raise = exc_to_raise or HttpExceptions.internal_server_error('An error occurred processing your request')

    target_exceptions = exceptions or (SQLAlchemyError, Exception)

    def __handle_unexpected_exceptions(cls):
        """
        This decorator handles SQLAlchemyError exception and unexpected exceptions,
        logs the error and raises HTTPException 500
        """
        for method_name in dir(cls):
            if not method_name.startswith('_'):
                method = getattr(cls, method_name)
                if callable(method):

                    setattr(
                        cls,
                        method_name,
                        __exception_handler(
                            method=method,
                            log_message=log_message,
                            exception_to_raise=exc_to_raise,
                            TargetExceptions=target_exceptions,
                        ),
                    )
        return cls

    return __handle_unexpected_exceptions
