from pathlib import Path
from .tbls import TBLSConfig
from strictyaml import load, Map, Str, Optional, Int
import json

INSERT_INTO = """


INSERT INTO {table_name} ({column_list})
VALUES
    {value_list}


"""

class Fixture:
    def __init__(self, fixture_dict, tbls_config):
        self._fix_dict = fixture_dict
        self._tbls_config = tbls_config

    def _value_list(self, data_dict, column_list):
        sql_text = ""
        items = list(data_dict.items())

        for pk, columns in items[:-1]:
            sql_text += "(" + str(pk) + ",'" + "','".join(columns.values()) + "'),\n    "

        pk, columns = items[-1]
        sql_text += "(" + str(pk) + ",'" + "','".join(columns.values()) + "');\n"

        return sql_text
            

    def sql(self):
        sql_text = ""
        
        for table, data_dict in self._fix_dict.items():
            column_list = self._tbls_config.column_list(table)
            sql_text += INSERT_INTO.format(
                table_name=table,
                column_list=", ".join(column_list),
                value_list=self._value_list(data_dict, column_list),
            )
        
        return sql_text

class HitchDb:
    def __init__(self, tbls_json_path: Path, fixture: Path):
        self._tbls_json_path = Path(tbls_json_path)
        self._fixture_path = Path(fixture)

        assert self._tbls_json_path.exists()
        assert self._fixture_path.exists()

    def sql(self):
        tbls_json = json.loads(self._tbls_json_path.read_text())
        assert tbls_json["driver"]["name"] == "postgres"
        
        tbls_config = TBLSConfig(tbls_json)
        
        fixture_dict = load(
            self._fixture_path.read_text(),
            tbls_config.strictyaml_schema()
        ).data
        fixture = Fixture(fixture_dict, tbls_config)
        return fixture.sql()
