all: build

build:
	docker build \
		--build-arg="REACT_APP_HOST=localhost" \
		--tag reactapp \
		.
	docker run \
		-d \
		--name reactapp \
		-p 80:3000 \
		reactapp

clean:
	docker stop reactapp
	docker rm reactapp
	docker rmi reactapp

re: clean build

.PHONY: build clean re