from logging import getLogger
from typing import Any, Dict, Union, List
import time 
import numpy as np 

from fastapi import APIRouter, BackgroundTasks
from src.ml.prediction import Data, classifier
from src.ml.outlier_detection import outlier_detector
from src.configurations import ServiceConfigurations 
from src.db import cruds, schemas
from src.db.database import get_context_db

logger = getLogger(__name__)
router = APIRouter()


@router.get("/health")
def health() -> Dict[str, str]:
    return {
        "health": "ok",
    }


@router.get("/metadata")
def metadata() -> Dict[str, Any]:
    return {
        "data_type": "str",
        "data_structure": (1, ),
        "data_sample": "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
        "prediction_type": "float32",
        "prediction_structure": (1,2),
        "prediction_sample": [0.97093159, 0.01558308],
    }


@router.get("/label")
def label() -> Dict[int, str]:
    return classifier.label


@router.get("/predict/test")
def predict_test() -> Dict[str, Any]:
    result = _predict(Data().data, "test", True)
    return result


@router.get("/predict/test/label")
def predict_test_label() -> Dict[str, Any]:
    result = _predict(Data().data, "test", False)
    return result 


@router.post("/predict")
def predict(data: Data, job_id: str, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    result = _predict(data.data, job_id, True)

    background_tasks.add_task(
        register_log,
        job_id,
        result,
        data
    )
    return result  


@router.post("/predict/label")
def predict_label(data: Data, job_id: str, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    result = _predict(data.data, job_id, False)
    
    background_tasks.add_task(
        register_log,
        job_id,
        result,
        data
    )
    return result 



######################################################################
# 推論器の予測
# 入力データの外れ値検知
def _predict(data: str, job_id: str, flg: bool) -> Dict[str, Any]:
    # 前処理
    input_ids: np.ndarray = classifier.transform(data)
    # 外れ値推論へのリクエスト
    result_class: Union[list, List[Dict[str, Any]]] = []
    start_outlier = time.time()
    is_outlier, outlier_score = outlier_detector.predict(input_ids)
    end_outlier = 1000 * (time.time() - start_outlier)

    # 分類推論へのリクエスト
    start_class = time.time()
    for service, url in ServiceConfigurations().services.items():
        result = {}
        logger.info(f"request to {url}")
        if flg:
            res = classifier.predict(input_ids, url)
        else:
            res = classifier.predict_label(input_ids, url)
        result[service] = res
        logger.info(f"input: {input_ids} output: {res}")
    result_class.append(result)
    end_class = 1000 * (time.time() - start_class)

    return {
        "job_id": job_id,
        "prediction": result_class,
        "prediction_elpased": end_class,
        "is_outlier": is_outlier,
        "outlier_score": outlier_score,
        "outlier_elpased": end_outlier
    }

###########################################################################
# ログデータベースへの書き込み
def register_log(job_id: str, result: Dict[str, Any], data: Data):
    with get_context_db() as db:
        prediction_log = {
            "prediction": result["prediction"],
            "prediction_elapsed": result["prediction_elpased"],
            "data": data.data
        }
        cruds.add_prediction_log(db=db, log_id=job_id, log=prediction_log, commit=True)

        outlier_log = {
            "is_outlier": result["is_outlier"],
            "outlier_score": result["outlier_score"],
            "outlier_elapsed": result["outlier_slpased"],
            "data": data.data
        }
        cruds.add_outlier_log(db=db, log_id=job_id, log=outlier_log, commit=True)
