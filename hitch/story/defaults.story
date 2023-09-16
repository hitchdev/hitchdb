#Default values for columns in fixtures:
  #docs: defaults
  #about: x
  #given:
    #postgres: |
      #CREATE TABLE core_users (
        #id integer primary key,
        #firstname varchar(50),
        #lastname varchar(50),
        #score int,
        #available bool,
        #age int
      #);
    #files:
      #hitchdb.yml: |
        #core_users:
          #defaults:
            #age: 30
            #score: 100
              
      #fixture.yml: |
        #core_users:
          #10:
            #firstname: Thomas
            #lastname: Beecham
            #available: yes
          #11:
            #firstname: Jane
            #lastname: O'Connor
            #available:
            
  #steps:
  #- Run tbls: |
      #{
        #"name": "postgres_db",
        #"desc": "",
        #"tables": [
          #{
            #"name": "public.core_users",
            #"type": "BASE TABLE",
            #"comment": "",
            #"columns": [
              #{
                #"name": "id",
                #"type": "integer",
                #"nullable": false,
                #"default": null,
                #"comment": ""
              #},
              #{
                #"name": "firstname",
                #"type": "varchar(50)",
                #"nullable": true,
                #"default": null,
                #"comment": ""
              #},
              #{
                #"name": "lastname",
                #"type": "varchar(50)",
                #"nullable": true,
                #"default": null,
                #"comment": ""
              #},
              #{
                #"name": "score",
                #"type": "integer",
                #"nullable": true,
                #"default": null,
                #"comment": ""
              #},
              #{
                #"name": "available",
                #"type": "boolean",
                #"nullable": true,
                #"default": null,
                #"comment": ""
              #},
              #{
                #"name": "age",
                #"type": "integer",
                #"nullable": true,
                #"default": null,
                #"comment": ""
              #}
            #],
            #"indexes": [
              #{
                #"name": "core_users_pkey",
                #"def": "CREATE UNIQUE INDEX core_users_pkey ON public.core_users USING btree (id)",
                #"table": "public.core_users",
                #"columns": [
                  #"id"
                #],
                #"comment": ""
              #}
            #],
            #"constraints": [
              #{
                #"name": "core_users_pkey",
                #"type": "PRIMARY KEY",
                #"def": "PRIMARY KEY (id)",
                #"table": "public.core_users",
                #"referenced_table": "",
                #"columns": [
                  #"id"
                #],
                #"referenced_columns": [],
                #"comment": ""
              #}
            #],
            #"triggers": [],
            #"def": ""
          #}
        #],
        #"relations": [],
        #"functions": [],
        #"driver": {
          #"name": "postgres",
          #"database_version": "PostgreSQL 13.0 on x86_64-pc-linux-musl, compiled by gcc (Alpine 9.3.0) 9.3.0, 64-bit",
          #"meta": {
            #"current_schema": "public",
            #"search_paths": [
              #"\"$user\"",
              #"public"
            #],
            #"dict": {
              #"Functions": "Stored procedures and functions"
            #}
          #}
        #}
      #}


  #- Run:
      #code: |
        #from hitchdb import HitchDb
        #from strictyaml import load
        #from path import Path

        #hitch_db = HitchDb("tbls.json", config="hitchdb.yml")

        #fixture = hitch_db.fixture(
            #load(
                #Path("fixture.yml").read_text(),
                #hitch_db.strictyaml_schema(),
            #).data
        #)

        #sql = fixture.sql()
        #print(sql)
        #Path("fixture.sql").write_text(sql)
      #will output: |-
        #INSERT INTO core_users (id, firstname, lastname, score, available, age)                                                                                         
        #VALUES                                                                                                                                                          
            #(10, 'Thomas', 'Beecham', 99, true, 18),                                                                                                                    
            #(11, 'Jane', 'O''Con%nor', 55, null, 19);

  #- run sql file:
      #filename: fixture.sql

  #- sql:
      #cmd: select * from core_users;
      #will output: |
        #podman-compose version: 1.0.6
        #['podman', '--version', '']
        #using podman version: 4.4.4
        #podman exec --interactive --tty --env POSTGRES_USER=postgres_user --env POSTGRES_PASSWORD=postgres_password --env POSTGRES_DB=postgres_db src_postgres_1 psql -U postgres_user postgres_db -c select * from core_users;
         #id | firstname | lastname  | score | available | age
        #----+-----------+-----------+-------+-----------+-----
         #10 | Thomas    | Beecham   |    99 | t         |  18
         #11 | Jane      | O'Con%nor |    55 |           |  19
        #(2 rows)

        #exit code: 0
