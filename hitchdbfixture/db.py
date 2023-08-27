from pathlib import Path
from strictyaml import load
import json


class HitchDbException(Exception):
    pass


class HitchDbFileError(HitchDbException):
    pass


class HitchDb:
    def __init__(self, tbls_json_path: Path, fixture: Path):
        self._tbls_json_path = Path(tbls_json_path)
        self._fixture_path = Path(fixture)

    def sql(self):
        tbls_json = json.loads(self._tbls_json_path.read_text())
        assert tbls_json["driver"]["name"] == "postgres"
        tbls_tables = tbls_json["tables"]

        tbl_dict = {
            tbl["name"].replace("public.", ""): tbl["columns"]
            for tbl in tbls_tables
        }
        fixture = load(self._fixture_path.read_text())
        #return json.dumps(tbl_dict, indent=4)
        return "x"
