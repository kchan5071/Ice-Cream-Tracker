
# username of user
USER_NAME := $(shell whoami)


start:
	pg_ctl -D /home/linuxbrew/.linuxbrew/var/postgresql@14 start

stop:
	pg_ctl -D /home/linuxbrew/.linuxbrew/var/postgresql@14 stop

create:
	createdb -h 127.0.0.1 -p 5432 -U $(USER_NAME) icecreamtracker
	psql -h 127.0.0.1 -p 5432 -d icecreamtracker -f database/database_tables_structure/icecreamtracker.sql

remove:
	dropdb -h 127.0.0.1 -p 5432 -U $(USER_NAME) icecreamtracker

connect:
	psql -h 127.0.0.1 -p 5432 -d icecreamtracker

# can view the tables once using \dt tracker.*