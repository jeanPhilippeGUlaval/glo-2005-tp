run:
	python3 server/main.py

init-bd-l:
	@sudo mysql -u root -p -e "source ./scripts/create_bd.sql"
	@echo "Success"

populate-l:
	@sudo mysql -u root -p -e "source ./scripts/addPorte.sql"
	@sudo mysql -u root -p -e "source ./scripts/addPanneaux.sql"
	@sudo mysql -u root -p -e "source ./scripts/addFerro.sql"

drop-bd-l:
	@sudo mysql -u root -p -e "source ./scripts/drop_bd.sql"
	@echo "BD Dropped"

init-bd:
	@mysql -u root -p -e "source ./scripts/create_bd.sql"
	@echo "Success"

populate:
	@mysql -u root -p -e "source ./scripts/addPorte.sql"

drop-bd:
	@mysql -u root -p -e "source ./scripts/drop_bd.sql"
	@echo "BD Dropped"