from pathlib import Path
from .tbls import TBLSConfig
from strictyaml import load, Map, Str, Optional, Int
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
        
        tbls_config = TBLSConfig(tbls_json)
        
        fixture = load(self._fixture_path.read_text())
        assert tbls_config.strictyaml_schema()
        #return json.dumps(tbl_dict, indent=4)
        return "x"
