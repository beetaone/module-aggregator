SHELL := /bin/bash

image:
	docker build -t weevagator .
.phony: image

run_image:
	docker run -p 8000:5000 --rm weevagator:latest
.phony: run_image

install_local:
	pip3 install -r requirements.txt
.phony: install_local

run_local:
	python3 weevagator.py
.phony: run_local