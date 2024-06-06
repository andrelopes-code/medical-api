from datetime import datetime, timezone


def get_timestamp():
    return datetime.now(timezone.utc)


def get_update_timestamp(_mapper, _connection, target):
    target.updated_at = datetime.now(timezone.utc)
