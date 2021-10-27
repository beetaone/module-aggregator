SHELL := /bin/bash
MODULE=weevenetwork/weeve-weevagator
create_image:
	docker build -t ${MODULE} . -f image/Dockerfile
.phony: create_image

create_and_push_multi_platform:
	docker buildx build --platform linux/amd64,linux/arm,linux/arm64 -t ${MODULE} --push . -f image/Dockerfile
.phony: create_and_push_multi_platform

push_latest:
	docker image push ${MODULE}
.phony: push_latest

run_image:
	docker run -p 5000:80 --rm --env-file=./config.env ${MODULE}:latest
.phony: run_image

lint:
	pylint main.py app/
.phony: lint

install_local:
	pip3 install -r image/requirements.txt
.phony: install_local

run_local:
	 python image/src/main.py
.phony: run_local