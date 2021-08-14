from src.configurations import ServiceConfigurations
import uuid
from logging import getLogger
import asyncio
from typing import Any, Dict, Tuple
import httpx
from pydantic import BaseModel 

from fastapi import APIRouter
from src.configurations import ServiceConfigurations, ServiceConfigurationsLightModel, ServiceConfigurationsSlowModel

logger = getLogger(__name__)
router = APIRouter()

class Data(BaseModel):
    data: str = "Lorem ipsum ."

@router.get("/health")
async def health() -> Dict[str, Dict[str, str]]:
    results = {}
    async with httpx.AsyncClient() as ac:

        async def req(ac, service, url) -> Tuple[str, dict]:
            response = await ac.get(f"{url}health")
            return service, response 
        tasks = [req(ac, service, url) for service, url in ServiceConfigurations().services.items()]

        responses = await asyncio.gather(*tasks)

        for service, res in responses:
            results[service] = res.json()

    return results 


@router.get("/metadata")
async def metadata() -> Dict[str, Dict[str, Any]]:
    results = {}
    async with httpx.AsyncClient() as ac:

        async def req(ac, service, url) -> Tuple[str, dict]:
            response = await ac.get(f"{url}metadata")
            return service, response 
        tasks = [req(ac, service, url) for service, url in ServiceConfigurations().services.items()]

        responses = await asyncio.gather(*tasks)

        for service, res in responses:
            results[service] = res.json()

    return results 

@router.post("/predict/test")
async def predict() -> Dict[str, dict]:
    job_id = str(uuid.uuid4())
    results = {}
    async with httpx.AsyncClient() as ac:
        async def req(ac, service, url, data, job_id):
            res = await ac.post(
                f"{url}predict", 
                json={"data": data.data},
                params={"job_id": job_id}
            )
            return service, res 
        tasks = [req(ac, service, url, Data(), job_id) for service, url in ServiceConfigurations().services.items()]
        responses = await asyncio.gather(*tasks)
        for service, res in responses:
            results[service] = res.json()
        return results 

@router.post("/predict/test/label")
async def predict() -> Dict[str, Dict[str, str]]:
    job_id = str(uuid.uuid4())
    results = {}
    async with httpx.AsyncClient() as ac:
        async def req(ac, service, url, data, job_id):
            res = await ac.post(
                f"{url}predict/label", 
                json={"data": data.data},
                params={"job_id": job_id}
            )
            return service, res 
        tasks = [req(ac, service, url, Data(), job_id) for service, url in ServiceConfigurationsLightModel().services.items()]
        responses = await asyncio.gather(*tasks)
        for service, res in responses:
            results[service] = res.json()
        return results 


@router.post("/predict")
async def predict(data: Data) -> Dict[str, Dict[str, Any]]:
    job_id = str(uuid.uuid4())
    results = {}
    async with httpx.AsyncClient() as ac:
        async def req(ac, service, url, data, job_id):
            res = await ac.post(
                f"{url}predict", 
                json={"data": data.data},
                params={"job_id": job_id}
            )
            return service, res 
        tasks = [req(ac, service, url, data, job_id) for service, url in ServiceConfigurations().services.items()]
        responses = await asyncio.gather(*tasks)
        for service, res in responses:
            results[service] = res.json()
        return results 


@router.post("/predict/label")
async def predict(data: Data) -> Dict[str, Dict[str, str]]:
    job_id = str(uuid.uuid4())
    results = {}
    async with httpx.AsyncClient() as ac:
        async def req(ac, service, url, data, job_id):
            res = await ac.post(
                f"{url}predict/label", 
                json={"data": data.data},
                params={"job_id": job_id}
            )
            return service, res 
        tasks = [req(ac, service, url, data, job_id) for service, url in ServiceConfigurationsLightModel().services.items()]
        responses = await asyncio.gather(*tasks)
        for service, res in responses:
            results[service] = res.json()
        return results 

@router.get("/job/{job_id}")
async def predict(job_id: str) -> Dict[str, Dict[str, Any]]:
    results = {}
    async with httpx.AsyncClient() as ac:
        async def req(ac, service, url, job_id):
            res = await ac.get(
                f"{url}job/{job_id}"
            )
            return service, res 
        tasks = [req(ac, service, url, job_id) for service, url in ServiceConfigurationsSlowModel().services.items()]
        responses = await asyncio.gather(*tasks)
        for service, res in responses:
            results[service] = res.json()
        return results 
