build:
	docker build -t mani --build-arg uid=`id -u` --build-arg gid=`id -g` --build-arg user=`whoami` -f docker/Dockerfile .
.PHONY: build

run:
	@docker compose -f docker/docker-compose.yml up
.PHONY: run

rundeps:
	@docker compose -f docker/docker-compose.dev.yml -f docker/docker-compose.yml up -d redis postgres
.PHONY: rundeps

rundev:
	@docker compose -f docker/docker-compose.dev.yml -f docker/docker-compose.yml up -d redis postgres
	@docker compose -f docker/docker-compose.dev.yml -f docker/docker-compose.yml up mani_app
.PHONY: rundev

shell:
	@docker exec -it mani_app python manage.py shell
.PHONY: shell

bash:
	@docker exec -it mani_app bash
.PHONY: bash

cssdev:
	@docker exec -u root -it mani_app tailwindcss -o ./static/tailwind.css --minify -w
.PHONY: cssdev

backup:
	@scp user@server:path/db.sqlite3 backup.sqlite3
.PHONY: backup

deploy:
	@sh deploy.sh
.PHONY: deploy

logs:
	@sh logs.sh
.PHONY: logs
