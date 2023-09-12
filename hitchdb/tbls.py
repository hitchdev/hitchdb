from strictyaml import Map, MapPattern, Int, Bool, Str, Float, Optional


class PrimaryKey:
    def __init__(self, column_name, column_type):
        self.column_name = column_name
        self.column_type = column_type 


class Table:
    def __init__(self, tbl_dict: dict):
        self._tbl_dict = tbl_dict

    @property
    def name(self):
        return self._tbl_dict["name"].replace("public.", "")

    def row_list(self, data):
        return [data[column["name"]] for column in self._tbl_dict["columns"][1:]]

    @property
    def columns(self) -> dict:
        return self._tbl_dict["columns"]

    def primary_key(self):
        constraints = self._tbl_dict["constraints"]
        primary_key_constraint_list = [
            constraint
            for constraint in constraints
            if constraint["type"] == "PRIMARY KEY"
        ]
        assert len(primary_key_constraint_list) == 1
        primary_key_constraint = primary_key_constraint_list[0]
        assert len(primary_key_constraint["columns"]) == 1
        pkey_name = primary_key_constraint["columns"][0]

        column_type = [
            column
            for column in self._tbl_dict["columns"]
            if column["name"] == pkey_name
        ][0]["type"]

        return PrimaryKey(
            column_name=pkey_name,
            column_type=column_type,
        )

    def _column_schema(self, column):
        if column["type"].startswith("varchar"):
            return Str()
        elif column["type"] in ("text", "uuid", "inet", "jsonb"):
            return Str()
        elif column["type"] in ("double precision"):
            return Float()
        elif column["type"].startswith("numeric"):
            return Float()
        elif column["type"] in ("integer", "bigint", "smallint"):
            return Int()
        elif column["type"] == "boolean":
            return Bool()
        elif column["type"] in ("timestamp with time zone", "date", "interval"):
            return Str()
        else:
            raise NotImplementedError(column["type"])

    def column_schemas(self):
        return Map(
            {
                column["name"]: self._column_schema(column)
                for column in self._tbl_dict["columns"]
                if column["name"] != self.primary_key().column_name
            }
        )

    def strictyaml_schema(self):
        primary_key = self.primary_key()
        return MapPattern(
            Int() if primary_key.column_type == "integer" else Str(),
            self.column_schemas(),
        )


class TBLSConfig:
    def __init__(self, tbls_json: dict):
        self._tj = tbls_json

        for table in tbls_json["tables"]:
            assert table["name"].startswith("public.")

        self._tbl_dict = {
            tbl_dict["name"].replace("public.", ""): Table(tbl_dict)
            for tbl_dict in tbls_json["tables"]
        }

    def column_list(self, table_name):
        return [col["name"] for col in self._tbl_dict[table_name].columns]

    def strictyaml_schema(self):
        return Map(
            {
                Optional(name): tbl.strictyaml_schema()
                for name, tbl in self._tbl_dict.items()
            }
        )
