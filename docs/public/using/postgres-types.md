---
title: Postgres Types
---
# Postgres Types



Demonstrate the use of various postgres specific types.


## Code Example


With postgres database set up with:

```sql
CREATE TABLE items (
  id integer primary key,
  mysmallint smallint,
  mybigint bigint,
  myuuid uuid,
  myinet inet,
  myjsonb jsonb,
  mydouble double precision,
  mynumeric numeric,
  mytimestamp timestamp with time zone,
  mydate date,
  myinterval interval
);

```


fixture.yml:

```yaml
items:
  10:
    mysmallint: 9
    mybigint: 10
    myuuid: 9fda6f42-6f3d-4ca5-a5e3-a72e91f746b2
    myinet: 127.0.0.1
    myjsonb: '{"x": "y"}'
    mydouble: 3.14159265354
    mynumeric: 3.14159265354
    mytimestamp: 2012-08-24 14:00:00 +02:00
    mydate: 2012-08-24
    myinterval: 10:00:00
  11:
    mysmallint: 10
    mybigint: 11
    myuuid: a25a2e85-0802-42d1-992b-24d8809c1eb0
    myinet: 127.0.0.2
    myjsonb: '{"a": "b"}'
    mydouble: 6.21494515439
    mynumeric: 6.21494515439
    mytimestamp: 2012-08-24 12:00:00 +00:00
    mydate: 2012-08-25
    myinterval: 11:00:00
    
```





Running tbls on this database will output:

```json
{
  "name": "postgres_db",
  "desc": "",
  "tables": [
    {
      "name": "public.items",
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
          "name": "mysmallint",
          "type": "smallint",
          "nullable": true,
          "default": null,
          "comment": ""
        },
        {
          "name": "mybigint",
          "type": "bigint",
          "nullable": true,
          "default": null,
          "comment": ""
        },
        {
          "name": "myuuid",
          "type": "uuid",
          "nullable": true,
          "default": null,
          "comment": ""
        },
        {
          "name": "myinet",
          "type": "inet",
          "nullable": true,
          "default": null,
          "comment": ""
        },
        {
          "name": "myjsonb",
          "type": "jsonb",
          "nullable": true,
          "default": null,
          "comment": ""
        },
        {
          "name": "mydouble",
          "type": "double precision",
          "nullable": true,
          "default": null,
          "comment": ""
        },
        {
          "name": "mynumeric",
          "type": "numeric",
          "nullable": true,
          "default": null,
          "comment": ""
        },
        {
          "name": "mytimestamp",
          "type": "timestamp with time zone",
          "nullable": true,
          "default": null,
          "comment": ""
        },
        {
          "name": "mydate",
          "type": "date",
          "nullable": true,
          "default": null,
          "comment": ""
        },
        {
          "name": "myinterval",
          "type": "interval",
          "nullable": true,
          "default": null,
          "comment": ""
        }
      ],
      "indexes": [
        {
          "name": "items_pkey",
          "def": "CREATE UNIQUE INDEX items_pkey ON public.items USING btree (id)",
          "table": "public.items",
          "columns": [
            "id"
          ],
          "comment": ""
        }
      ],
      "constraints": [
        {
          "name": "items_pkey",
          "type": "PRIMARY KEY",
          "def": "PRIMARY KEY (id)",
          "table": "public.items",
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
INSERT INTO items (id, mysmallint, mybigint, myuuid, myinet, myjsonb, mydouble, mynumeric, mytimestamp, mydate, myinterval)                                     
VALUES                                                                                                                                                          
    (10, 9, 10, '9fda6f42-6f3d-4ca5-a5e3-a72e91f746b2', '127.0.0.1', '{"x": "y"}', 3.14159265354, 3.14159265354, '2012-08-24 14:00:00 +02:00', '2012-08-24', '10
:00:00'),                                                                                                                                                       
    (11, 10, 11, 'a25a2e85-0802-42d1-992b-24d8809c1eb0', '127.0.0.2', '{"a": "b"}', 6.21494515439, 6.21494515439, '2012-08-24 12:00:00 +00:00', '2012-08-25', '1
1:00:00');
```




Then the file fixture.sql is run.

Then running:

```sql
select * from items;
```

Will output:
```
podman-compose version: 1.0.6
['podman', '--version', '']
using podman version: 4.4.4
podman exec --interactive --tty --env POSTGRES_USER=postgres_user --env POSTGRES_PASSWORD=postgres_password --env POSTGRES_DB=postgres_db src_postgres_1 psql -U postgres_user postgres_db -c select * from items;
 id | mysmallint | mybigint |                myuuid                |  myinet   |  myjsonb   |   mydouble    |   mynumeric   |      mytimestamp       |   mydate   | myinterval
----+------------+----------+--------------------------------------+-----------+------------+---------------+---------------+------------------------+------------+------------
 10 |          9 |       10 | 9fda6f42-6f3d-4ca5-a5e3-a72e91f746b2 | 127.0.0.1 | {"x": "y"} | 3.14159265354 | 3.14159265354 | 2012-08-24 12:00:00+00 | 2012-08-24 | 10:00:00
 11 |         10 |       11 | a25a2e85-0802-42d1-992b-24d8809c1eb0 | 127.0.0.2 | {"a": "b"} | 6.21494515439 | 6.21494515439 | 2012-08-24 12:00:00+00 | 2012-08-25 | 11:00:00
(2 rows)

exit code: 0

```






!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchdb/blob/master/hitch/story/postgres-types.story">postgres-types.story
    storytests.</a>

