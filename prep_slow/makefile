DOCKER_REPOSITORY := kooose/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
IMAGE_VERSION := 0.0.1

TEMPLATE_PATTERN := prep_slow
TEMPLATE_PATTERN_PORT := 7000


.PHONY: build
build:
	docker build \
		-t $(DOCKER_REPOSITORY):$(TEMPLATE_PATTERN)_$(IMAGE_VERSION) \
		-f $(DOCKERFILE) \
		.

.PHONY: push
push:
	docker push $(DOCKER_REPOSITORY):$(TEMPLATE_PATTERN)_$(IMAGE_VERSION)

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
