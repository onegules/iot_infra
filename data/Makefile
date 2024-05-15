VERSION := 0.1.0
SHELL := /bin/bash


.PHONY: generate_protos
generate_protos: 
	buf generate

.PHONY: push
push:
	buf push --tag v${VERSION}
