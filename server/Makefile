all: run-dev

run-prod: install-dependencies
	uvicorn main:app --host 0.0.0.0 --port 8888

run-dev: install-dependencies
	uvicorn main:app --reload

install-dependencies:
	pip install -r requirements.txt

clean:
	rm -rf __pycache__

re: clean run-dev

.PHONY: run-prod run-dev install-dependencies clean re