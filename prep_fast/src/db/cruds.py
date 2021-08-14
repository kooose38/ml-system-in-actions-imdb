
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