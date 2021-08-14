import os
from logging import getLogger

from src.constants import CONSTANTS, PLATFORM_ENUM

logger = getLogger(__name__)


class PlatformConfigurations:
    platform = os.getenv("PLATFORM", PLATFORM_ENUM.DOCKER.value)
    if not PLATFORM_ENUM.has_value(platform):
        raise ValueError(f"PLATFORM must be one of {[v.value for v in PLATFORM_ENUM.__members__.values()]}")


class DBConfigurations:
    mysql_username = os.getenv("MYSQL_USER")
    mysql_password = os.getenv("MYSQL_PASSWORD")
    mysql_port = int(os.getenv("MYSQL_PORT", 3306))
    mysql_database = os.getenv("MYSQL_DATABASE", "log_db")
    mysql_server = os.getenv("MYSQL_SERVER")
    sql_alchemy_database_url = (
        f"mysql://{mysql_username}:{mysql_password}@{mysql_server}:{mysql_port}/{mysql_database}?charset=utf8"
    )


class APIConfigurations:
    title = os.getenv("API_TITLE", "ServingPattern")
    description = os.getenv("API_DESCRIPTION", "machine learning system serving patterns")
    version = os.getenv("API_VERSION", "0.1")


logger.info(f"{PlatformConfigurations.__name__}: {PlatformConfigurations.__dict__}")
logger.info(f"{APIConfigurations.__name__}: {APIConfigurations.__dict__}")