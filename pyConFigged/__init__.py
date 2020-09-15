
from typing import Any
from pyConFigged.backend import Backend, IniBackend
from pyConFigged.exceptions import *

INI_BACKEND = IniBackend


class ConfigDict:

    def __init__(self, path: str, data_backend=None, autocommit=False, readonly=False):
        data_backend = data_backend or INI_BACKEND
        self._backend = data_backend(path)
        self._data = self._clean(self._backend.read())
        self.readonly = readonly
        self.autocommit = autocommit

    def __getitem__(self, item) -> Any:
        if item in self._data:
            return self._data[item]

    def __setitem__(self, key, value):
        if self.readonly:
            raise ReadOnlyError
        self._data[key] = value
        if self.autocommit:
            self.commit()

    def commit(self) -> None:
        self._backend.write(self._data)

    def _clean(self, data: dict) -> dict:
        clean_dict = {}
        for key, value in data.items():
            if isinstance(value, dict):
                clean_dict[key] = self._clean(value)
            else:
                clean_dict[key] = value.strip('"').strip("'")
        return clean_dict




if __name__ == "__main__":

    cd = ConfigDict("..//test.ini", INI_BACKEND)

    print(cd["section_one"]["val1"])

    pass