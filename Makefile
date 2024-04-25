isort:
	isort

black:
	black .

lint: isort black

check_and_rename_env:
	  @if [ -e ".env" ]; then \
        echo "env file exists."; \
      else \
      	cp .env.example .env | \
        echo "File does not exist."; \
      fi

build: check_and_rename_env
	docker compose build


build_cuda: check_and_rename_env
	docker compose  -f docker_compose.gpu.yml build


run_build :
		docker compose build

run_build_gpu :
		docker compose -f docker_compose.gpu.yml up

