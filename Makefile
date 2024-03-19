run:
	python3 main.py

init-bd:
	@sudo mysql -u root -py -e "source ./scripts/create_bd.sql"
	@echo "Success"

drop-bd:
	@sudo mysql -u root -py -e "source ./scripts/drop_bd.sql"
	@echo "BD Dropped"