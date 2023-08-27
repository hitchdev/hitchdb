Quickstart:
  docs: quickstart
  about: x
  given:
    postgres: |
      CREATE TABLE users (
        id integer,
        name varchar(50)
      );
    files:
      fixture.yml: |
        users:
          10:
            name: Thomas
  steps:
  - Run tbls: |
      {
        "name": "postgres_db",
        "desc": "",
        "tables": [
          {
            "name": "public.users",
            "type": "BASE TABLE",
            "comment": "",
            "columns": [
              {
                "name": "id",
                "type": "integer",
                "nullable": true,
                "default": null,
                "comment": ""
              },
              {
                "name": "name",
                "type": "varchar(50)",
                "nullable": true,
                "default": null,
                "comment": ""
              }
            ],
            "indexes": [],
            "constraints": [],
            "triggers": [],
            "def": ""
          }
        ],
        "relations": [],
        "functions": [],
        "driver": {
          "name": "postgres",
          "database_version": "PostgreSQL 13.0 on x86_64-pc-linux-musl, compiled by gcc (Alpine 9.3.0) 9.3.0, 64-bit",
          "meta": {
            "current_schema": "public",
            "search_paths": [
              "\"$user\"",
              "public"
            ],
            "dict": {
              "Functions": "Stored procedures and functions"
            }
          }
        }
      }


  - Run:
      code: |
        from hitchdbfixture import HitchDb
        from path import Path

        fixture = HitchDb(
            schema="tbls.json",
            fixture="fixture.yml",
        )
        print(fixture.sql())
      will output: x

  #- SQL:
      #on: postgres
      #cmd: select * from users;
      #will output: x
