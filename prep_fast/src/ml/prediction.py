import json
from logging import getLogger
from typing import Dict
import requests
import base64

import numpy as np
from onnx import numpy_helper
from pydantic import BaseModel
from google.protobuf.json_format import MessageToJson
from src.configurations import ModelConfigurations
from src.ml.transform import prep 

logger = getLogger(__name__)


class Data(BaseModel):
    data: str = "Lorem Ipsum is simply dummy text of the printing and typesetting industry."


class Classifier(object):
    def __init__(
        self,
        preprocessing_path: str,
        label_filepath: str,
        input_name: str,
        output_name: str,
    ):
        self.preprocessing_path = preprocessing_path
        self.label_filepath: str = label_filepath
        self.label: Dict[str, str] = {}
        self.input_name: str = input_name 
        self.output_name: str = output_name 

        self.prep = None 
        self.load_model()
        self.load_label()

    def load_model(self):
        logger.info(f"load preprocess in {self.preprocessing_path}")
        self.prep = prep 
        logger.info(f"initialized preprocess")

    def load_label(self):
        logger.info(
            f"load label in {self.label_filepath}",
        )
        with open(self.label_filepath, "r") as f:
            self.label = json.load(f)
        logger.info(f"label: {self.label}")

    def transform(self, data: str) -> np.ndarray:
        input_ids = self.prep.transform(data)
        input_ids = np.array(input_ids).astype(np.float32)
        return input_ids 

    def predict(self, input_ids: np.ndarray, endpoint: str) -> np.ndarray:
        '''onnxruntime-serverへのREST形式でリクエストする'''
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # JSON形式のリクエスト
        tensor_proto = numpy_helper.from_array(input_ids) 

        json_str = MessageToJson(tensor_proto, use_integers_for_enums=True)  # TensorProtoをJSON形式に変換
        data = json.loads(json_str)

        inputs = {
            self.input_name: data 
        }
        output_filters = [self.output_name]  # 保存時に指定した出力層の名前

        payload = {}  # リクエストで送るペイロードの作成、 inputs と outputFilter のフィールドをそれぞれ埋める
        payload["inputs"] = inputs
        payload["outputFilter"] = output_filters

        res = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        raw_data = json.loads(res.text)['outputs'][self.output_name]['rawData']  # 生データを取得
        output = np.frombuffer(base64.b64decode(raw_data), dtype=np.float32)  # 生データはbase64でencodeされたバイナリ列なので適切にdecode
        logger.info(output) # (batch, tag_size)形式で返る
        return output 

    def predict_label(self, input_ids: np.ndarray, endpoint: str) -> str:
        prediction = self.predict(input_ids, endpoint)
        argmax = int(np.argmax(np.array(prediction)))
        return self.label[str(argmax)]


classifier = Classifier(
    preprocessing_path=ModelConfigurations().preprocessing_transformers_path,
    label_filepath=ModelConfigurations().label_filepath,
    input_name=ModelConfigurations().onnx_input_name,
    output_name=ModelConfigurations().onnx_output_name,
)