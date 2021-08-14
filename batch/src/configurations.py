import logging
import os
from logging import getLogger
from typing import Dict 

from src.constants import CONSTANTS, PLATFORM_ENUM

logger = logging.getLogger(__name__)

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

class CacheConfigurations:
    cache_host = os.getenv("CACHE_HOST", "redis")
    cache_port = int(os.getenv("CACHE_PORT", 6379))
    queue_name = os.getenv("QUEUE_NAME", "queue")


class RedisCacheConfigurations(CacheConfigurations):
    redis_db = int(os.getenv("REDIS_DB", 0))
    redis_decode_responses = bool(os.getenv("REDIS_DECODE_RESPONSES", True))

class ModelConfigurations:
    onnx_input_name_1 = os.getenv("ONNX_INPUT_NAME_1", "input_ids")
    onnx_input_name_2 = os.getenv("ONNX_INPUT_NAME_2", "token_type_ids")
    onnx_input_name_3 = os.getenv("ONNX_INPUT_NAME_3", "attention_mask")
    onnx_output_name = os.getenv("ONNX_OUTPUT_NAME", "output")
    label_path = os.getenv("LABEL_FILEPATH", "/batch/models/labels.json")

logger.info(f"{ServiceConfigurations.__name__}: {ServiceConfigurations.__dict__}")
logger.info(f"{PlatformConfigurations.__name__}: {PlatformConfigurations.__dict__}")
logger.info(f"{CacheConfigurations.__name__}: {CacheConfigurations.__dict__}")
logger.info(f"{RedisCacheConfigurations.__name__}: {RedisCacheConfigurations.__dict__}")
