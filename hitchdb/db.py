from hitchdb.tbls import TBLSConfig
from hitchdb.fixture import Fixture
from pathlib import Path


class HitchDb:
    def __init__(self, tbls_json_path: Path):
        self._tbls_config = TBLSConfig(Path(tbls_json_path))

    def strictyaml_schema(self):
        return self._tbls_config.strictyaml_schema()

    def fixture(self, data: dict):
        assert isinstance(data, dict)
        return Fixture(
            data,
            self._tbls_config,
        )
