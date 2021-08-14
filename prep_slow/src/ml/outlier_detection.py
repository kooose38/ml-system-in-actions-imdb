from logging import getLogger
from typing import Any, Tuple
from sklearn.preprocessing import PowerTransformer

import numpy as np
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
       '''対数変換と正規分布化する'''
       data = np.log1p(data)
       pt = PowerTransformer(method="yao-johnson")
       data = pt.fit_transform(data)
       return data 

    def predict(self, data: np.ndarray) -> Tuple[bool, float]:
        '''One-Class推論器へのリクエスト'''
        # prep_fastの入力データ前処理(ボキャブラリー数)と異なるため別のsvm推論器を用意しています
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