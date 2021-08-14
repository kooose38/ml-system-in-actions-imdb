FROM mcr.microsoft.com/onnxruntime/server:latest

ARG SERVER_DIR=rnn_onnx_runtime
ENV PROJECT_DIR imdb_classification
ENV MODEL_BASE_PATH=${PROJECT_DIR}/models

WORKDIR /${PROJECT_DIR}

COPY ./bert_imdb.onnx /${MODEL_BASE_PATH}/bert_imdb.onnx
ENV MODEL_PATH /${MODEL_BASE_PATH}/bert_imdb.onnx

WORKDIR /onnxruntime/server/
COPY ./onnx_runtime_server_entrypoint.sh ./onnx_runtime_server_entrypoint.sh
RUN chmod +x onnx_runtime_server_entrypoint.sh
ENTRYPOINT ["./onnx_runtime_server_entrypoint.sh"]