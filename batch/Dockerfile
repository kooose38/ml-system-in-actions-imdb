FROM python:3.8-slim

ENV PROJECT_DIR batch
WORKDIR /${PROJECT_DIR}
ADD ./requirements.txt /${PROJECT_DIR}/
RUN apt-get -y update && \
    apt-get -y install apt-utils gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

COPY ./src/ /${PROJECT_DIR}/src/
COPY ./models/ /${PROJECT_DIR}/models/

ENV LOG_LEVEL DEBUG
ENV LOG_FORMAT TEXT

CMD [ "python", "-m", "src.backend.prediction_batch.py" ]