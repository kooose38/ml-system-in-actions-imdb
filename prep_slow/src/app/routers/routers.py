from logging import getLogger
from src.db.database import get_context_db
from typing import Any, Dict
import numpy as np 
import time 

from fastapi import APIRouter, BackgroundTasks
from src.ml.transform import Data
from src.ml.transform import prep 
from src.backend import background_job, store_data_job
from src.ml.outlier_detection import outlier_detector
from src.db import cruds, schemas

logger = getLogger(__name__)
router = APIRouter()


@router.get("/health")
def health() -> Dict[str, str]:
    return {
        "health": "ok",
    }


@router.get("/metadata"):
def metadata() -> Dict[str, Any]:
    return {
        "data_type": "str",
        "data_structure": (1, ),
        "data_sample": "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
        "prediction_type": "float32",
        "prediction_structure": (1,2),
        "prediction_sample": [0.97093159, 0.01558308],
    }


@router.post("/predict")
def predict(data: Data, job_id: str, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    result = _predict(data, job_id, background_tasks)
    
    background_tasks.add_tasks(
        register_log,
        job_id,
        result,
        data
    )
    return result


@router.get("/job/{job_id}")
def prediction_resuls(job_id: str) -> Dict[str, Any]:
    '''バッチ推論された結果の取得とログの更新'''
    pred_label: str = store_data_job.get_data_redis(job_id)
    result = _get_predict(job_id, pred_label)
    return result




##############################################################################################
def _predict(data: Data, job_id: str, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    '''redisに接続して入力データの登録をする+入力データの外れ値検知を推論する'''
    input_ids: Dict[str, np.ndarray] = prep.transform(data.data)

    start_outlier = time.time()
    is_outlier, outlier_score = outlier_detector.predict(input_ids["input_ids"])
    end_outlier = 1000 * (time.time() - start_outlier)

    start_db = time.time()
    background_job.save_data_job(input_ids, job_id, background_tasks, True)
    end_db = 1000 * (time.time() - start_db)

    return {
        "job_id": job_id,
        "prediction": "",
        "prediction_elapsed": end_db,
        "is_outlier": is_outlier,
        "outlier_score": outlier_score,
        "outlier_elapsed": end_outlier
    }


def register_log(job_id: str, result: Dict[str, Any], data: Data):
    '''mysqlに接続してログを貯める'''
    with get_context_db() as db:
        prediction_log = {
            "prediction": result["prediction"],
            "prediction_elapsed": result["prediction_elapsed"],
            "data": data.data 
        }
        cruds.add_prediction_log(db=db, log_id=job_id, log=prediction_log, commit=True)

        outlier_log = {
            "is_outlier": result["is_outlier"],
            "outlier_score": result["outlier_score"],
            "outlier_elapsed": result["outlier_elapsed"],
            "data": data.data
        }
        cruds.add_outlier_log(db=db, log_id=job_id, log=outlier_log, commit=True)



##########################################################################################
def _get_predict(job_id: str, pred_label: str):
    '''job_idをKeyにmysqlから取得して推論結果の更新をする'''
    with get_context_db() as db:
        outlier_log = cruds.select_outlier_by_id(db=db, log_id=job_id)
        prediction_log = cruds.select_prediction_by_id(db=db, log_id=job_id)
        cruds.updata_prediction(db=db, log_id=job_id, prediction=pred_label)

    return {
        "job_id": job_id,
        "prediction": pred_label,
        "prediction_elapsed": prediction_log.log["prediction_elapsed"],
        "is_outlier": outlier_log.log["is_outlier"],
        "outlier_score": outlier_log.log["outlier_log"],
        "outlier_elapsed": outlier_log.log["outlier_elapsed"]
    }


