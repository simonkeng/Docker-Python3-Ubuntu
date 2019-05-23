default: image

all: image py_3.6.8

image:
	docker build -f Dockerfile \
	--build-arg PYTHON_VERSION_TAG=3.7.3 \
	--build-arg LINK_PYTHON_TO_PYTHON3=1 \
	-t ubuntu18python37:latest \
	--compress .

