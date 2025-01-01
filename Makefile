shell:
	docker exec -it backend python crm/manage.py shell

makemigrations:
	docker exec backend python crm/manage.py makemigrations

migrate:
	docker exec backend python crm/manage.py migrate

format:
	docker exec backend /bin/bash -c 'black . && isort crm/ && autoflake --remove-all-unused-imports --ignore-init-module-imports -i -r .'

test:
	docker exec backend python crm/manage.py test crm/

init_data:
	docker exec backend python crm/manage.py initialize_data
