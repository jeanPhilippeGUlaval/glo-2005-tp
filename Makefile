run:
	python3 main.py

init-bd-l:
	@sudo mysql -u root -py -e "source ./scripts/create_bd.sql"
	@echo "Success"

drop-bd-l:
	@sudo mysql -u root -py -e "source ./scripts/drop_bd.sql"
	@echo "BD Dropped"

init-bd:
	@mysql -u root -py -e "source ./scripts/create_bd.sql"
	@echo "Success"

drop-bd:
	@mysql -u root -py -e "source ./scripts/drop_bd.sql"
	@echo "BD Dropped"