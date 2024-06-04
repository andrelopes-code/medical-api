
format:
	isort .
	black .

up:
	docker compose up -d
	docker compose logs api --follow

sh:
	docker compose exec api bash

test:
	docker compose exec test pytest -vxs

pre-commit:
	make format
	git add .

alembic-upgrade:
	docker compose exec api alembic upgrade head

alembic-downgrade:
	docker compose exec api alembic downgrade -1

alembic-base:
	docker compose exec api alembic downgrade base