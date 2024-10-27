include .env

db-up:
	sudo docker compose up -d

db-down:
	sudo docker compose down --volumes --rmi all

db-down-rmi:
	sudo make db-down
	sudo rm -rf ${MYSQL_VOLUME}

db-logs:
	sudo docker compose logs -f

db-dump:
	sudo docker exec ${MYSQL_CONTAINER_NAME} /usr/bin/mysqldump -u root --password=${MYSQL_ROOT_PASSWORD} ${MYSQL_DATABASE} > $(location)

db-restore:
	cat $(location) | sudo docker exec -i ${MYSQL_CONTAINER_NAME} /usr/bin/mysql -u root --password=${MYSQL_ROOT_PASSWORD} ${MYSQL_DATABASE}

db-healthcheck:
	sudo docker exec ${MYSQL_CONTAINER_NAME} mysqladmin ping -u root --password=${MYSQL_ROOT_PASSWORD}
