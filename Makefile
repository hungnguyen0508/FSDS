# Variables 
DB_SERVICE=postgres_db
DB_COMPOSE_FILE=docker-compose.yml
INGEST_SCRIPT=ingest_data.py
DB_HOST=localhost
DB_PORT=5433
DB_NAME=football_db
DB_USER=postgres
DB_PASSWORD=meomeomeo123
DBT_PROFILES_DIR=./transformation/football_prediction
BACKEND_SERVICE=backend
FRONTEND_SERVICE=frontend


# Mark these names as not files
.PHONY: all db up ingest transformation backend frontend down full-refresh

all: db ingest transformation backend frontend

# 1. Start database container
db: 
	docker compose -f $(DB_COMPOSE_FILE) up -d db 


# 2. ingest data using ingest_data.py file
ingest: db 
	@echo "Waiting 10s for DB to be ready ...."
	sleep 10
	@echo "Running ingestion script ..."
	DATABASE_URL="postgresql://$(DB_USER):$(DB_PASSWORD)@$(DB_HOST):$(DB_PORT)/$(DB_NAME)" \
		python $(INGEST_SCRIPT)
# 3. transform data, create medallion-structure schemas using dbt 
transformation: ingest 
	@echo "running dbt full-refresh to transform data..."
	dbt run --profiles-dir $(DBT_PROFILES_DIR) --full-refresh

backend: dbt
	docker compose -f $(DB_COMPOSE_FILE) up -d $(BACKEND_SERVICE)

# 5. Start frontend container
frontend: backend
	docker compose -f $(DB_COMPOSE_FILE) up -d $(FRONTEND_SERVICE)

# 6. Stop and remove all containers
down:
	docker compose -f $(DB_COMPOSE_FILE) down

