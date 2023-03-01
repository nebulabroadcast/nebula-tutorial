COMPOSE=$(shell which docker-compose || echo "docker compose")
SERVER_IMAGE=nebulabroadcast/nebula-server:latest
WORKER_IMAGE=nebulabroadcast/nebula-worker:latest
SERVER_CONTAINER=backend
WORKER_CONTAINER=worker

.PHONY: dbshell setup reload

#
# Runtime
#

dbshell:
	@$(COMPOSE) exec postgres psql -U nebula nebula

setup:
	@$(COMPOSE) exec $(SERVER_CONTAINER) python -m setup
	@$(COMPOSE) exec $(SERVER_CONTAINER) ./manage reload

reload:
	@$(COMPOSE) exec $(SERVER_CONTAINER) ./manage reload

restart:
	@$(COMPOSE) restart $(SERVER_CONTAINER) $(WORKER_CONTAINER)

update:
	docker pull $(SERVER_IMAGE)
	docker pull $(WORKER_IMAGE)

	$(COMPOSE) up --detach --build $(SERVER_CONTAINER)
	$(COMPOSE) up --detach --build $(WORKER_CONTAINER)

user:
	@$(COMPOSE) exec $(SERVER_CONTAINER) python -m cli user

password:
	@$(COMPOSE) exec $(SERVER_CONTAINER) python -m cli password
