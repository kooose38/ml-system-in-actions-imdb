import logging
from typing import Any, Dict

from src.backend.redis_client import redis_client

logger = logging.getLogger(__name__)

def make_image_key(key: str) -> str:
    return f"{key}_image"


def left_push_queue(queue_name: str, key: str) -> bool:
    try:
        redis_client.lpush(queue_name, key)
        return True
    except Exception:
        return False


def right_pop_queue(queue_name: str) -> Any:
    if redis_client.llen(queue_name) > 0:
        return redis_client.rpop(queue_name)
    else:
        return None


def set_data_redis(key: str, value: Dict[str, str]) -> bool:
    redis_client.set(key, value)
    return True


def get_data_redis(key: str) -> Any:
    data = redis_client.get(key)
    return data


def set_image_redis(key: str, results: dict) -> str:
    image_key = make_image_key(key)
    redis_client.set(image_key, results)
    return image_key


