from hitchdb.tbls import TBLSConfig
from hitchdb.fixture import Fixture
from pathlib import Path
import json


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
