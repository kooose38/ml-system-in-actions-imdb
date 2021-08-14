DOCKER_REPOSITORY := kooose/ml-system-in-actions

DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yml
IMAGE_VERSION := 0.0.1

PREP_PRED_PATTERN := rnn_imdb_classification

.PHONY: build
build:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PREP_PRED_PATTERN)_$(IMAGE_VERSION)  .

.PHONY: push
push: 
	docker push $(DOCKER_REPOSITORY):$(PREP_PRED_PATTERN)_$(IMAGE_VERSION)

.PHONY: c_up
c_up:
	docker-compose \
		-f ./$(DOCKER_COMPOSE) \
		up -d

.PHONY: c_down
c_down:
	docker-compose \
		-f ./$(DOCKER_COMPOSE) \
		down
