from strictyaml import Map, MapPattern, Int, Str

class TBLSConfig:
    def __init__(self, tbls_json: dict):
        self._tj = tbls_json

        for table in tbls_json["tables"]:
            assert table["name"].startswith("public.")

        self._tbl_dict = {
            tbl["name"].replace("public.", ""): tbl["columns"]
            for tbl in tbls_json["tables"]
        }


    def _schema_for_table(self, columns):
        return MapPattern(
            Int(),
            MapPattern(Str(), Str())
        )

    def strictyaml_schema(self):
        return Map({
            name: self._schema_for_table(columns)
            for name, columns in self._tbl_dict.items()
        })
