from transformers import BertTokenizer
import torch
from typing import Dict 
import numpy as np 
from pydantic import BaseModel

from src.configurations import ModelConfigurations


class Data(BaseModel):
  data: str = "Lorem ipsum ."

class PreprocessingBertModel:
  def __init__(self, filename: str) -> Dict[str, np.ndarray]:
    self.tokenizer = BertTokenizer(vocab_file=filename, do_lower_case=True)

  def transform(self, text: str, max_length=256):
    text_list = []
    for r in text.strip().split():
       r = r.replace("\n", " ")
       r = r.replace("\r", "")
       r = r.replace(".", " . ")
       r = r.replace(",", " , ")
       text_list.append(r)
    
    encoding = self.tokenizer(" ".join(text_list), max_length=max_length, padding="max_length", return_tensors="pt")
    encoding = {k: np.array(v).astype(np.float32) for k, v in encoding.items()}
    return encoding

prep  = PreprocessingBertModel(ModelConfigurations().vocab_file)