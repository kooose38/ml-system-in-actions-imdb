import asyncio
import logging
import os
from concurrent.futures import ProcessPoolExecutor
from ml.prediction import classifier
from time import sleep
from typing import Dict 

from src.backend import store_data_job
from src.configurations import CacheConfigurations, ServiceConfigurations

log_format = logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s")
logger = logging.getLogger("prediction_batch")
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(log_format)
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)


def _trigger_prediction_if_queue(services: Dict[str, str]):
    job_id = store_data_job.right_pop_queue(CacheConfigurations.queue_name)
    logger.info(f"predict job_id: {job_id}")
    if job_id is not None:
        data = store_data_job.get_data_redis(job_id)
        if data != "":
            return True
        image_key = store_data_job.make_image_key(job_id)
        image_data = store_data_job.get_data_redis(image_key)
        results = {}

        for service, url in services.items():
            response = classifier.predict_label(image_data, url)
            results[service] = response 
            logger.info(f"input: {data} output: {response}")

        if len(results) != 0:
            return store_data_job.set_data_redis(job_id, results)
        else:
            return store_data_job.left_push_queue(CacheConfigurations.queue_name, job_id)


def _loop():
    services = ServiceConfigurations().services 

    while True:
        sleep(1)
        _trigger_prediction_if_queue(services)


def prediction_loop(num_procs: int = 2):
    executor = ProcessPoolExecutor(num_procs)
    loop = asyncio.get_event_loop()

    for _ in range(num_procs):
        asyncio.ensure_future(loop.run_in_executor(executor, _loop))

    loop.run_forever()


def main():
    NUM_PROCS = int(os.getenv("NUM_PROCS", 2))
    prediction_loop(NUM_PROCS)


if __name__ == "__main__":
    logger.info("start backend")
    main()