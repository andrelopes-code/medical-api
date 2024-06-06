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
