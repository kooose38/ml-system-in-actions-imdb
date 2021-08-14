#!/bin/bash

set -eu

HTTP_PORT=${HTTP_PORT:-8001}
GRPC_PORT=${GRPC_PORT:-50051}
LOGLEVEL=${LOGLEVEL:-"debug"}
NUM_HTTP_THREADS=${NUM_HTTP_THREADS:-4}
MODEL_PATH=${MODEL_PATH:-"/imdb_classification/models/rnn_imdb.onnx"}

./onnxruntime_server \
    --http_port=${HTTP_PORT} \
    --grpc_port=${GRPC_PORT} \
    --num_http_threads=${NUM_HTTP_THREADS} \
    --model_path=${MODEL_PATH} 