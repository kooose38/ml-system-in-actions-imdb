DOCKER_REPOSITORY := kooose/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yml
IMAGE_VERSION := 0.0.1

PREDICTION_MONITORING_PATTERN := monitor

.PHONY: build
build:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PREDICTION_MONITORING_PATTERN)_$(IMAGE_VERSION) .


.PHONY: push
push:
	docker push $(DOCKER_REPOSITORY):$(PREDICTION_MONITORING_PATTERN)_$(IMAGE_VERSION)

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