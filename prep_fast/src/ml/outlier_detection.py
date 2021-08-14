from logging import getLogger
from typing import Any, Tuple

import numpy as np
from sklearn.preprocessing import PowerTransformer
import requests 
import json 
from src.configurations import ServiceConfiguraionsOutlier

logger = getLogger(__name__)

class OutlierDetector(object):
    def __init__(self, model_path: str):
       self.endpoint = model_path 
       self.headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
       }

    def transform(self, data: np.ndarray) -> np.ndarray:
       '''対数変換＋正規分布化'''
       data = np.log1p(data)
       pt = PowerTransformer(method="yao-johnson")
       data = pt.fit_transform(data)
       return data

    def predict(self, data: Any) -> Tuple[bool, float]:
        np_data = np.array(data).astype(np.float32)
        np_data = self.transform(np_data)
        data = {"data": np_data}
        res = requests.post(self.endpoint, data=json.dumps(data), headers=self.headers)
        res = res.json()
        is_outlier = res["is_outlier"]
        outlier_score = res["outlier_score"]
        return is_outlier, outlier_score

outlier_detector = OutlierDetector(
   model_path=ServiceConfiguraionsOutlier().outlier_url
)
