from typing import List

from sqlalchemy.orm import Session
from src.db import models, schemas


def select_prediction_log_between(
    db: Session,
    time_before: str,
    time_later: str,
) -> List[schemas.PredictionLog]:
    return (
        db.query(models.PredictionLog)
        .filter(models.PredictionLog.created_datetime >= time_before)
        .filter(models.PredictionLog.created_datetime <= time_later)
        .all()
    )


def select_outlier_log_between(
    db: Session,
    time_before: str,
    time_later: str,
) -> List[schemas.OutlierLog]:
    return (
        db.query(models.OutlierLog)
        .filter(models.OutlierLog.created_datetime >= time_before)
        .filter(models.OutlierLog.created_datetime <= time_later)
        .all()
    )