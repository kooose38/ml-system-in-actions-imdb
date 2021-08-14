import logging
from typing import Any
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



def set_data_redis(key: str, value: str) -> bool:
    redis_client.set(key, value)
    return True


def get_data_redis(key: str) -> Any:
    data = redis_client.get(key)
    return data


def set_image_redis(key: str, data: Any) -> str:
    image_key = make_image_key(key)
    redis_client.set(image_key, data)
    return image_key


def save_image_redis_job(job_id: str, data: Any) -> bool:
    set_image_redis(job_id, data)
    redis_client.set(job_id, "")
    return True
