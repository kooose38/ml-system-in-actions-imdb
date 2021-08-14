from logging import getLogger
from typing import Any, Dict

from fastapi import APIRouter
from src.ml.prediction import Data, classifier

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
        "data_type": "int64",
        "data_structure": "(1,512, dtype=np.ndarray)",
        "data_sample": [[2, 2, 34, 23, 222, 23, 0, 0, 0]],
        "prediction_type": "float32",
        "prediction_structure": (1,2),
        "prediction_sample": [0.97093159, 0.01348537],
    }

@router.post("/predict/test")
def predict() -> Dict[str, float]:
    results = {}
    is_outlier, outlier_score = classifier.predict(Data().data)
    results["is_outlier"] = is_outlier
    results["outlier_score"] = outlier_score 
    logger.info(f"from outlier model: [{Data().data}] [{is_outlier}]")
    return results 

@router.post("/predict")
def predict(data) -> Dict[str, float]:
    '''BertModelの入力データに対して外れ値検知を行う'''
    results = {}
    is_outlier, outlier_score = classifier.predict(data.data)
    results["is_outlier"] = is_outlier
    results["outlier_score"] = outlier_score 
    logger.info(f"from outlier model: [{data.data}] [{is_outlier}]")
    return results 