from typing import Dict, Any

from sqlalchemy.orm import Session
from src.db import models, schemas

def add_prediction_log(
    db: Session,
    log_id: str,
    log: Dict[str, Any],
    commit: bool = True,
) -> schemas.PredictionLog:
    data = models.PredictionLog(
        log_id=log_id,
        log=log,
    )
    db.add(data)
    if commit:
        db.commit()
        db.refresh(data)
    return data


def add_outlier_log(
    db: Session,
    log_id: str,
    log: Dict[str, Any],
    commit: bool = True,
) -> schemas.OutlierLog:
    data = models.OutlierLog(
        log_id=log_id,
        log=log,
    )
    db.add(data)
    if commit:
        db.commit()
        db.refresh(data)
    return data


def select_prediction_by_id(
    db: Session,
    log_id: str
) -> schemas.PredictionLog:
    return db.query(models.PredictionLog).filter(models.PredictionLog.log_id == log_id).first()
    

def select_outlier_by_id(
    db: Session,
    log_id: str
) -> schemas.OutlierLog:
    return db.query(models.OutlierLog).filter(models.OutlierLog.log_id == log_id).first()


def updata_prediction(
    db: Session,
    log_id: str,
    prediction: str
) -> schemas.PredictionLog:
    data = select_prediction_by_id(db, log_id)
    data.log["prediction"] = prediction
    db.commit()
    db.refresh(data)
    return data 
