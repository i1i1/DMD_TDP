# Innopolis. Data Modeling and Databases I<br/>Project Codename "The Durka"

To install:
``` sh
$ git clone https://github.com/i1i1/DMD_TDP
```
To run use `docker-compose`:
``` sh
$ docker-compose up --build
```
Warning: to run on Windows, convert all files to unix format.

Server is started at localhost:80

After you stoped the docker, run `docker-compose down` before next launch:
``` sh
$ docker-compose down
```

# Structure of the project

* `queries` directory contains 5 specified queries
* `db.py` initializes database
* `generate_data.py` script for automatic creation of insert statements
* `init.sql` contains database schema
* `main.py` incorporates all functionality with GUI

