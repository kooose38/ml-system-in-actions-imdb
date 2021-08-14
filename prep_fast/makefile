DOCKER_REPOSITORY := kooose/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
IMAGE_VERSION := 0.0.1
DOCKER_COMPOSE := docker-compose.yml

TEMPLATE_PATTERN := prep_fast
TEMPLATE_PATTERN_PORT := 8000


.PHONY: build
build:
	docker build \
		-t $(DOCKER_REPOSITORY):$(TEMPLATE_PATTERN)_$(IMAGE_VERSION) \
		-f $(DOCKERFILE) \
		.
	 
.PHONY: run
run:
	docker run \
		-d \
		--name $(TEMPLATE_PATTERN) \
		-p $(TEMPLATE_PATTERN_PORT):$(TEMPLATE_PATTERN_PORT) \
		$(DOCKER_REPOSITORY):$(TEMPLATE_PATTERN)_$(IMAGE_VERSION)

.PHONY: rm 
rm:
	docker rm -f $(TEMPLATE_PATTERN)

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