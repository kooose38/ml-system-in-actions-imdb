from logging import getLogger
from typing import Tuple

import numpy as np
import onnxruntime as rt
from pydantic import BaseModel
from src.configurations import ModelConfigurations

logger = getLogger(__name__)


class Data(BaseModel):
    data: np.ndarray = np.random.randint(1, 3000, 128).reshape(1, -1)


class Classifier(object):
    def __init__(
        self,
        model_filepath: str,
    ):
        self.model_filepath: str = model_filepath
        self.classifier = None
        self.input_name: str = ""
        self.output_name: str = ""

        self.load_model()

    def load_model(self):
        logger.info(f"load model in {self.model_filepath}")
        self.classifier = rt.InferenceSession(
            self.model_filepath,
        )
        # inputの数に応じて追加する
        self.input_name = self.classifier.get_inputs()[0].name
        self.output_name = self.classifier.get_outputs()[0].name
        logger.info(f"initialized model")

    def predict(self, data: np.ndarray) -> Tuple[bool, float]:
        prediction = self.classifier.run(
            None, 
            {self.input_name: np.array(data).reshape(1, -1).astype(np.float32)},
        )
        output = float(prediction[1][0][0])
        is_outlier = output < 0.0
        logger.info(f"predict proba {output}")
        return output, is_outlier 


classifier = Classifier(
    model_filepath=ModelConfigurations().model_filepath,
)