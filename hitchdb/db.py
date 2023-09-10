from hitchdb.tbls import TBLSConfig
from pathlib import Path
import json


INSERT_INTO = """


INSERT INTO {table_name} ({column_list})
VALUES
    {value_list}


"""


def sqlformat(scalar):
    if isinstance(scalar, str):
        return f"'{scalar}'"
    elif isinstance(scalar, int):
        return str(scalar)
    elif isinstance(scalar, bool):
        return "true" if scalar else "false"
    else:
        raise NotImplementedError("Unknown type")


def formatted(data_list):
    return [sqlformat(x) for x in data_list]


class Fixture:
    def __init__(self, fixture_dict, tbls_config):
        self._fix_dict = fixture_dict
        self._tbls_config = tbls_config

    def _value_list(self, table, data_dict, column_list):
        tbl = self._tbls_config._tbl_dict[table]
        sql_text = ""
        items = list(data_dict.items())

        for pk, data in items[:-1]:
            row_list = formatted(tbl.row_list(data))
            sql_text += "(" + str(pk) + ", " + ", ".join(row_list) + "),\n    "

        pk, data = items[-1]
        row_list = formatted(tbl.row_list(data))
        sql_text += "(" + str(pk) + ", " + ", ".join(row_list) + ");\n"

        return sql_text

    def sql(self):
        sql_text = ""

        for table, data_dict in self._fix_dict.items():
            column_list = self._tbls_config.column_list(table)
            sql_text += INSERT_INTO.format(
                table_name=table,
                column_list=", ".join(column_list),
                value_list=self._value_list(table, data_dict, column_list),
            )

        return sql_text


class HitchDb:
    def __init__(self, tbls_json_path: Path):
        self._tbls_json_path = Path(tbls_json_path)

        assert self._tbls_json_path.exists()
        tbls_json = json.loads(self._tbls_json_path.read_text())
        assert tbls_json["driver"]["name"] == "postgres", (
            "HitchDb currently only works for postgres.\n"
            "Raise a ticket for mysql/mariadb/"
            "microsoft sql server/sqllite/bigquery/redshift/dynamodb"
        )

        self._tbls_config = TBLSConfig(tbls_json)

    def strictyaml_schema(self):
        return self._tbls_config.strictyaml_schema()

    def fixture(self, data: dict):
        assert isinstance(data, dict)
        return Fixture(
            data,
            self._tbls_config,
        )
