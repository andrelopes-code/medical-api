from typing import Union

from pydantic import BaseModel


def update_model_fields(model: BaseModel, data: Union[dict, BaseModel]):
    """Updates the given model fields with the given data"""
    if isinstance(data, dict):
        # use case for dict
        for field, value in data.items():
            if value is not None:
                setattr(model, field, value)
    else:
        # use case for SQLModel
        for field, value in data:
            if value is not None:
                setattr(model, field, value)
