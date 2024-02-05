all: up

up:
	docker run \
		-d \
		--name mongo \
		-p 27017:27017 \
		-e MONGO_INITDB_ROOT_USERNAME=user \
		-e MONGO_INITDB_ROOT_PASSWORD=passwd \
		mongo

down:
	docker stop mongo

clean: down
	docker rm mongo
	docker rmi mongo

fclean: clean
	rm -rf ./database/data/*
	rm -rf ./database/data/.mongodb

re: clean up

.PHONY: up down clean fclean re