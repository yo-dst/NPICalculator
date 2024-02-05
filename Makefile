all: up

up:
	mkdir -p database/data
	docker-compose up -d --build

down:
	docker-compose down

clean: down
	docker system prune -af

fclean: clean
	rm -rf ./database/data/*
	rm -rf ./database/data/.mongodb

re: clean up

.PHONY: up down clean re