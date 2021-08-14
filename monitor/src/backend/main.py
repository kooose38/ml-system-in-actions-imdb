import datetime
import time
from logging import DEBUG, Formatter, StreamHandler, getLogger
from typing import List

import click
from src.db import cruds, schemas
from src.db.database import get_context_db

logger = getLogger(__name__)
logger.setLevel(DEBUG)
formatter = Formatter("[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s")

handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)


def evaluate_prediction(
    prediction_logs: List[schemas.PredictionLog],
):
    logger.info("evaluate predictions...")
    logger.info(f"prediction num {len(prediction_logs)}")
    for  p in prediction_logs:
       logger.info("-"*30)
       logger.info(f"log_id: {p.log_id}")
       logger.info(f"log: {p.log}")
       logger.info(f"created at: {p.created_datetime}")
    logger.info("done evaluating predictions")


def evaluate_outlier(
    outlier_threshold: float,
    outlier_logs: List[schemas.OutlierLog],
):
    '''入力データの外れ値が一定値以上でエラーログの出力をする'''
    logger.info("evaluate outliers...")
    logger.info(f"outlier num {len(outlier_logs)}")
    outliers = 0
    for o in outlier_logs:
        logger.info("-"*30)
        logger.info(f"log_id: {o.log_id}")
        logger.info(f"log: {o.log}")
        logger.info(f"created at: {o.created_datetime}")
        if o.log["is_outlier"]:
            outliers += 1
    if outliers > len(outlier_logs) * outlier_threshold:
        logger.error(f"too many outliers: {outliers}")
    logger.info("done evaluating outliers")


@click.command(name="request job")
@click.option("--interval", type=int, default=1)
@click.option("--threshold", type=float, default=0.2)
def main(
    interval: int,
    threshold: float,
):
    '''1分毎にログの出力'''
    logger.info("start monitoring...")
    while True:
        now = datetime.datetime.now()
        interval_ago = now - datetime.timedelta(minutes=(interval + 1))
        time_later = now.strftime("%Y-%m-%d %H:%M:%S")
        time_before = interval_ago.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"time between {time_before} and {time_later}")
        with get_context_db() as db:
            prediction_logs = cruds.select_prediction_log_between(db=db, time_before=time_before, time_later=time_later)
            outlier_logs = cruds.select_outlier_log_between(db=db, time_before=time_before, time_later=time_later)
        logger.info(f"prediction_logs between {time_before} and {time_later}: {len(prediction_logs)}")
        logger.info(f"outlier_logs between {time_before} and {time_later}: {len(outlier_logs)}")
        if len(prediction_logs) > 0:
            evaluate_prediction(prediction_logs)
        if len(outlier_logs) > 0:
            evaluate_outlier(threshold, outlier_logs)
        time.sleep(interval * 60)


if __name__ == "__main__":
    main()