include .env
export

#========================#
#== DATABASE MIGRATION ==#
#========================#

## Run migrations UP
migrate-up:
	docker compose -f ${DOCKER_COMPOSE_FILE} --profile tools run --rm migrate up

migrate-up-force:
	docker compose -f ${DOCKER_COMPOSE_FILE} --profile tools run --rm migrate up force $(version)

migrate-down: ## Rollback migrations against non test DB
	docker compose -f ${DOCKER_COMPOSE_FILE} --profile tools run --rm migrate down 1

migrate-create: ## Create a DB migration files e.g `make migrate-create name=migration-name`
	docker compose -f ${DOCKER_COMPOSE_FILE} --profile tools run --rm migrate create -ext sql -dir /migrations $(name)

shell-db: ## Enter to database console
	docker compose -f ${DOCKER_COMPOSE_FILE} exec db psql -U postgres -d postgres


