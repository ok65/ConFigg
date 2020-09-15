
from typing import Dict, Any
import configparser
from multiprocessing import Lock


class Backend:

    def __init__(self, path: str):
        self.path = path

    def read(self) -> Dict[str, Any]:
        raise NotImplementedError

    def write(self, wr_dict: Dict[str, Any]) -> None:
        raise NotImplementedError


class IniBackend(Backend):

    def __init__(self, path: str):
        super().__init__(path)
        self.lock = Lock()

    def read(self) -> Dict[str, Any]:
        parser = configparser.ConfigParser()
        parser.read(self.path)
        data = {}
        for section_name, section_dict in parser._sections.items():
            data[section_name] = section_dict
        return data

    def write(self, data: Dict[str, Any]) -> None:
        self.lock.acquire(False)
        with open(self.path, "w+") as fp:
            parser = configparser.ConfigParser()
            parser.read_dict(data)
            parser.write(fp)
        self.lock.release()
