import os
from logging import getLogger
from typing import Dict 

from src.constants import CONSTANTS, PLATFORM_ENUM

logger = getLogger(__name__)


class PlatformConfigurations:
    platform = os.getenv("PLATFORM", PLATFORM_ENUM.DOCKER.value)
    if not PLATFORM_ENUM.has_value(platform):
        raise ValueError(f"PLATFORM must be one of {[v.value for v in PLATFORM_ENUM.__members__.values()]}")


class ServiceConfigurations:
    services: Dict[str, str] = {}
    for environ in os.environ.keys():
        if environ.startswith("SERVICE_"):
            url = str(os.getenv(environ))
            services[environ.lower().replace("service_", "")] = url


class ServiceConfiguraionsOutlier:
    outlier_url = os.getenv("OUTLIER_URL", "http://localhost:8003/predict")


class APIConfigurations:
    title = os.getenv("API_TITLE", "ServingPattern")
    description = os.getenv("API_DESCRIPTION", "machine learning system serving patterns")
    version = os.getenv("API_VERSION", "0.1")


class ModelConfigurations:
    preprocessing_transformers_path = os.getenv(
        "PREPROCESSING_TRANSFORMERS_PATH", "/prep_fast/models/vocab_file.txt"
    )
    label_filepath = os.getenv("LABEL_FILEPATH", "/prep_fast/models/labels.json")

    onnx_input_name = os.getenv("ONNX_INPUT_NAME", "input_ids")
    onnx_output_name = os.getenv("ONNX_OUTPUT_NAME", "output")


class DBConfigurations:
    mysql_username = os.getenv("MYSQL_USER")
    mysql_password = os.getenv("MYSQL_PASSWORD")
    mysql_port = int(os.getenv("MYSQL_PORT", 3306))
    mysql_database = os.getenv("MYSQL_DATABASE", "log_db")
    mysql_server = os.getenv("MYSQL_SERVER")
    sql_alchemy_database_url = (
        f"mysql://{mysql_username}:{mysql_password}@{mysql_server}:{mysql_port}/{mysql_database}?charset=utf8"
    )



logger.info(f"{PlatformConfigurations.__name__}: {PlatformConfigurations.__dict__}")
logger.info(f"{APIConfigurations.__name__}: {APIConfigurations.__dict__}")
logger.info(f"{ModelConfigurations.__name__}: {ModelConfigurations.__dict__}")
logger.info(f"{ServiceConfiguraionsOutlier.__name__}: {ServiceConfiguraionsOutlier.__dict__}")
logger.info(f"{ServiceConfigurations.__name__}: {ServiceConfigurations.__dict__}")
logger.info(f"{DBConfigurations.__name__}: {DBConfigurations.__dict__}")
