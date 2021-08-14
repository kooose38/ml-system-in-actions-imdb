import json
import base64
from logging import getLogger
from typing import Any, Dict
import requests 
from google.protobuf.json_format import MessageToJson

import numpy as np
from onnx import numpy_helper
from src.configurations import ModelConfigurations

logger = getLogger(__name__)


class Classifier(object):
    def __init__(
        self,
        input_name_1: str,
        input_name_2: str,
        input_name_3: str,
        output_name: str,
        label_path
    ):
        self.input_name_1: str = input_name_1
        self.input_name_2: str = input_name_2
        self.input_name_3: str = input_name_3 
        self.output_name: str = output_name 
        self.label_path: str = label_path
        self.label = {}
        self.load_label()
   
    def load_label(self):
         with open(self.label_path, "r") as f:
            self.label = json.load(f)
         f.close()
         logger.info(f"labels: {self.label}")

    def transform(self, data: Any):
       data = np.array(data).astype(np.float32)
       tensor_proto = numpy_helper.form_array(data)

       json_str = MessageToJson(tensor_proto, use_integers_for_enums=True)
       data = json.loads(json_str)
       return data 


    def predict(self, data: Dict[str, np.ndarray], endpoint: str) -> np.ndarray:
       headers = {
         'Content-Type': 'application/json',
         'Accept': 'application/json'
      }
       input_ids = self.transform(data["input_ids"])
       token_type_ids = self.transform(data["token_type_ids"])
       attention_mask = self.transform(data["attention_mask"])

       inputs = {
            self.input_name_1: input_ids, 
            self.input_name_2: token_type_ids,
            self.input_name_3: attention_mask
        }

       payload = {"inputs": inputs, "outputFilter": [self.output_name]}

       res = requests.post(endpoint, headers=headers, data=json.dumps(payload))
       logger.info(res)
       raw_data = json.loads(res.text)["output"][self.output_name]["rawData"]
       # output.shape == (batch, tag_size)
       output = np.frombuffer(base64.b64decode(raw_data), dtype=np.float32)
       logger.info(output)
       return output 

    def predict_label(self, data: Any, endpoint: str) -> str:
        prediction = self.predict(data, endpoint)
        argmax = int(np.argmax(np.array(prediction)))
        return self.label[str(argmax)]


classifier = Classifier(
    input_name_1=ModelConfigurations().onnx_input_name_1,
    input_name_2=ModelConfigurations().onnx_input_name_2,
    input_name_3=ModelConfigurations().onnx_input_name_3,
    output_name=ModelConfigurations().onnx_output_name,
    label_path=ModelConfigurations().label_path
)
