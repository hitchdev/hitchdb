---
title: Quickstart
---
# Quickstart



x

## Code Example


With postgres database set up with:

```sql
CREATE TABLE core_users (
  id integer primary key,
  firstname varchar(50),
  lastname varchar(50),
  score int,
  available bool,
  age int
);

```


fixture.yml:

```yaml
core_users:
  10:
    firstname: Thomas
    lastname: Beecham
    age: 18
    score: 99
    available: yes
  11:
    age: 19
    firstname: Jane
    available:
    lastname: O'Connor
    score: 55
    
```





Running tbls on this database will output:

```json
{
  "name": "postgres_db",
  "desc": "",
  "tables": [
    {
      "name": "public.core_users",
      "type": "BASE TABLE",
      "comment": "",
      "columns": [
        {
          "name": "id",
          "type": "integer",
          "nullable": false,
          "default": null,
          "comment": ""
        },
        {
          "name": "firstname",
          "type": "varchar(50)",
          "nullable": true,
          "default": null,
          "comment": ""
        },
        {
          "name": "lastname",
          "type": "varchar(50)",
          "nullable": true,
          "default": null,
          "comment": ""
        },
        {
          "name": "score",
          "type": "integer",
          "nullable": true,
          "default": null,
          "comment": ""
        },
        {
          "name": "available",
          "type": "boolean",
          "nullable": true,
          "default": null,
          "comment": ""
        },
        {
          "name": "age",
          "type": "integer",
          "nullable": true,
          "default": null,
          "comment": ""
        }
      ],
      "indexes": [
        {
          "name": "core_users_pkey",
          "def": "CREATE UNIQUE INDEX core_users_pkey ON public.core_users USING btree (id)",
          "table": "public.core_users",
          "columns": [
            "id"
          ],
          "comment": ""
        }
      ],
      "constraints": [
        {
          "name": "core_users_pkey",
          "type": "PRIMARY KEY",
          "def": "PRIMARY KEY (id)",
          "table": "public.core_users",
          "referenced_table": "",
          "columns": [
            "id"
          ],
          "referenced_columns": [],
          "comment": ""
        }
      ],
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

```


```python
from hitchdb import HitchDb
from strictyaml import load
from path import Path

hitch_db = HitchDb("tbls.json")

fixture = hitch_db.fixture(
    load(
        Path("fixture.yml").read_text(),
        hitch_db.strictyaml_schema(),
    ).data
)

sql = fixture.sql()
print(sql)
Path("fixture.sql").write_text(sql)

```

Will output:
```
INSERT INTO core_users (id, firstname, lastname, score, available, age)                                                                                         
VALUES                                                                                                                                                          
    (10, 'Thomas', 'Beecham', 99, true, 18),                                                                                                                    
    (11, 'Jane', 'O''Connor', 55, null, 19);
```




Then the file fixture.sql is run.

Then running:

```sql
select * from core_users;
```

Will output:
```
podman-compose version: 1.0.6
['podman', '--version', '']
using podman version: 4.4.4
podman exec --interactive --tty --env POSTGRES_USER=postgres_user --env POSTGRES_PASSWORD=postgres_password --env POSTGRES_DB=postgres_db src_postgres_1 psql -U postgres_user postgres_db -c select * from core_users;
 id | firstname | lastname | score | available | age
----+-----------+----------+-------+-----------+-----
 10 | Thomas    | Beecham  |    99 | t         |  18
 11 | Jane      | O'Connor |    55 |           |  19
(2 rows)

exit code: 0

```






!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchdb/blob/master/hitch/story/quickstart.story">quickstart.story
    storytests.</a>

