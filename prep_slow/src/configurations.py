import os
from logging import getLogger

from src.constants import CONSTANTS, PLATFORM_ENUM

logger = getLogger(__name__)


class PlatformConfigurations:
    platform = os.getenv("PLATFORM", PLATFORM_ENUM.DOCKER.value)
    if not PLATFORM_ENUM.has_value(platform):
        raise ValueError(f"PLATFORM must be one of {[v.value for v in PLATFORM_ENUM.__members__.values()]}")

class CacheConfigurations:
    cache_host = os.getenv("CACHE_HOST", "redis")
    cache_port = int(os.getenv("CACHE_PORT", 6379))
    queue_name = os.getenv("QUEUE_NAME", "queue")


class RedisCacheConfigurations(CacheConfigurations):
    redis_db = int(os.getenv("REDIS_DB", 0))
    redis_decode_responses = bool(os.getenv("REDIS_DECODE_RESPONSES", True))


class APIConfigurations:
    title = os.getenv("API_TITLE", "ServingPattern")
    description = os.getenv("API_DESCRIPTION", "machine learning system serving patterns")
    version = os.getenv("API_VERSION", "0.1")

class ModelConfigurations:
    vocab_file = os.getenv("VOCAB_FILE", "/prep_slow/models/en-vocab-bert.txt")


class DBConfigurations:
    mysql_username = os.getenv("MYSQL_USER")
    mysql_password = os.getenv("MYSQL_PASSWORD")
    mysql_port = int(os.getenv("MYSQL_PORT", 3306))
    mysql_database = os.getenv("MYSQL_DATABASE", "log_db")
    mysql_server = os.getenv("MYSQL_SERVER")
    sql_alchemy_database_url = (
        f"mysql://{mysql_username}:{mysql_password}@{mysql_server}:{mysql_port}/{mysql_database}?charset=utf8"
    )


class ServiceConfigurationsOutlier:
    outlier_url = os.getenv("OUTLIER_URL", "http://localhost:7003/predict")


logger.info(f"{PlatformConfigurations.__name__}: {PlatformConfigurations.__dict__}")
logger.info(f"{APIConfigurations.__name__}: {APIConfigurations.__dict__}")
logger.info(f"{DBConfigurations.__name__}: {DBConfigurations.__dict__}")
logger.info(f"{ModelConfigurations.__name__}: {ModelConfigurations.__dict__}")
logger.info(f"{ServiceConfigurationsOutlier.__name__}: {ServiceConfigurationsOutlier.__dict__}")
logger.info(f"{RedisCacheConfigurations.__name__}: {RedisCacheConfigurations.__dict__}")
