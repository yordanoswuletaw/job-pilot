include .env

$(eval export $(shell sed -ne 's/ *#.*$$//; /./ s/=.*$$// p' .env))

export PYTHONPATH := $(shell pwd)/src

init: # Setup a poetry virtual environment for first time
	poetry config virtualenvs.in-project true
	poetry init
	poetry shell

install: # Create a local Poetry virtual environment and install all required Python dependencies.
	poetry env use 3.11
	poetry install

help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done


# ======================================
# ------- Docker Infrastructure --------
# ======================================
local-start: # Build and start your local Docker infrastructure.
	docker compose -f docker-compose.yml up --build -d

local-stop: # Stop your local Docker infrastructure.
	docker compose -f docker-compose.yml down --remove-orphans

local-restart: # Restart your local Docker infrastructure.
	docker compose -f docker-compose.yml down --remove-orphans
	docker compose -f docker-compose.yml up --build -d


# ======================================
# ---------- Run Piplines -------------
# ======================================
local-run: # run piplines
	cd src/ && poetry run python -m main