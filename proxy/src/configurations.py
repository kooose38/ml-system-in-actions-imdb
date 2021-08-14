import os
from logging import getLogger
from typing import Dict 

from src.constants import PLATFORM_ENUM

logger = getLogger(__name__)


class PlatformConfigurations:
    platform = os.getenv("PLATFORM", PLATFORM_ENUM.DOCKER.value)
    if not PLATFORM_ENUM.has_value(platform):
        raise ValueError(f"PLATFORM must be one of {[v.value for v in PLATFORM_ENUM.__members__.values()]}")


class APIConfigurations:
    title = os.getenv("API_TITLE", "ServingPattern")
    description = os.getenv("API_DESCRIPTION", "machine learning system serving patterns")
    version = os.getenv("API_VERSION", "0.1")

class ServiceConfigurationsLightModel:
    services: Dict[str, str] = {}
    for env in os.environ.keys():
        if env.startswith("SERVICE_FAST_"):
            url = str(os.getenv(env))
            services[env.lower().replace("service_", "")] = url 

class ServiceConfigurationsSlowModel:
    services: Dict[str, str] = {}
    for env in os.environ.keys():
        if env.startswith("SERVICE_SLOW_"):
            url = str(os.getenv(env))
            services[env.lower().replace("service_", "")] = url 

class ServiceConfigurations:
    services: Dict[str, str] = {}
    for env in os.environ.keys():
        if env.startswith("SERVICE_"):
            url = str(os.getenv(env))
            services[env.lower().replace("service_", "")] = url 



logger.info(f"{PlatformConfigurations.__name__}: {PlatformConfigurations.__dict__}")
logger.info(f"{APIConfigurations.__name__}: {APIConfigurations.__dict__}")
logger.info(f"{ServiceConfigurationsLightModel.__name__}: {ServiceConfigurationsLightModel.__dict__}")
logger.info(f"{ServiceConfigurationsSlowModel.__name__}: {ServiceConfigurationsSlowModel.__dict__}")
logger.info(f"{ServiceConfigurations.__name__}: {ServiceConfigurations.__dict__}")
