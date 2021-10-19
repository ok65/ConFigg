
import unittest
import os
from configg import Configg
from configg.exceptions import *
from configg.ini_backend import IniBackend
from configg.json_backend import JsonBackend
from configg.xml_backend import XmlBackend


class CommonTests(unittest.TestCase):
    config_dict = None
    config_data = {"section_one": {"val1": "Stuff", "val2": "apples"},
                   "section_two": {"val3": "oranges", "val4": 12} }

    def edit_file(self):
        raise NotImplemented

    def instance(self, options=None):
        raise NotImplemented

    @staticmethod
    def file_path():
        raise NotImplemented

    def setUp(self) -> None:
        self.config_dict = self.instance()

    def tearDown(self) -> None:
        self.config_dict = None

    def test_read1(self):
        self.assertEqual(self.config_dict.section_one["val1"], "Stuff")
        self.assertEqual(self.config_dict.section_one["val2"], "apples")
        self.assertEqual(self.config_dict.section_two["val3"], "oranges")

    def test_write_manual(self):
        self.config_dict.section_one["new_entry"] = "new value"
        self.config_dict.commit()
        cd2 = self.instance()
        self.assertEqual(cd2.section_one["new_entry"], "new value")

    def test_write_auto(self):
        cd_auto = self.instance({"autocommit": True})
        cd_auto.add_section("section_three", {"val10": "apricots"})
        cd_read = self.instance()
        self.assertEqual(cd_read.section_three["val10"], "apricots")

    def test_add_section(self):
        self.config_dict.add_section("new_section", {"bird": "duck"})
        self.assertEqual(self.config_dict.new_section["bird"], "duck")

    def test_reload(self):
        self.edit_file()
        self.assertNotIn("val5", self.config_dict.section_two)
        self.config_dict.reload()
        self.assertEqual(self.config_dict.section_two["val5"], "potato")

    def test_addremove_section(self):
        self.config_dict.add_section("dummy", {"bird": "goose"})
        self.assertIn("dummy", self.config_dict.sections)
        self.config_dict.remove_section("dummy")
        self.assertNotIn("dummy", self.config_dict.sections)

    def test_readonly_error(self):

        def test_write(cd):
            cd.section_two["val5"] = "pineapple"

        cd_ro = self.instance({"readonly": True})
        self.assertRaises(ReadOnlyError, lambda: test_write(cd_ro))

    def test_keys(self):
        self.assertSetEqual(set(self.config_dict.section_one.keys()), {"val1", "val2"})

    def test_items(self):
        self.assertSetEqual(set(self.config_dict.section_one.values()), {"Stuff", "apples"})

    def test_defaults(self):
        self.default_config = self.instance({'defaults':{"default_section": {"bird": "robin"}}})
        self.assertIn("default_section", self.default_config.sections)
        self.assertEqual(self.default_config.default_section["bird"], "robin")

class IniTests(CommonTests):


    @classmethod
    def setUpClass(cls) -> None:
        with open(cls.file_path(), "w+") as fp:
            fp.write("[section_one] \n"
                     "val1 = Stuff \n"
                     "val2 = apples \n"
                     "[section_two] \n"
                     "val3 = oranges \n"
                     "val4 = 12 ")

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(cls.file_path())

    def instance(self, options=None) -> Configg:
        return Configg(self.file_path(), data_backend=IniBackend, **options or {})

    def edit_file(self):
        with open(self.file_path(), "a+") as fp:
            fp.write("""\nval5 = potato""")

    @staticmethod
    def file_path():
        return "unittest.ini"


class JsonTests(CommonTests):

    @classmethod
    def setUpClass(cls) -> None:
        with open(cls.file_path(), "w+") as fp:
            fp.write("""{"section_one": {"val1": "Stuff",
                                         "val2": "apples"},
                         "section_two": {"val3": "oranges",
                                         "val4": 12}}""")

    def instance(self, options=None) -> Configg:
        return Configg(self.file_path(), data_backend=JsonBackend, **options or {})

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(cls.file_path())

    def edit_file(self):
        with open(self.file_path(), "w+") as fp:
            fp.write("""{"section_one": {"val1": "Stuff",
                                         "val2": "apples"},
                         "section_two": {"val3": "oranges",
                                         "val4": 12,

                                             "val5": "potato"}}""")
    @staticmethod
    def file_path():
        return "unittest.json"

class XmlTests(CommonTests):

    @classmethod
    def setUpClass(cls) -> None:
        with open(cls.file_path(), "w+") as fp:
            fp.write("<config>"
                        "<section_one>"
                            "<val1>Stuff</val1>"
                            "<val2>apples</val2>"
                        "</section_one>"
                        "<section_two>"
                            "<val3>oranges</val3>"
                            "<val4>12</val4>"
                        "</section_two>"
                    "</config>")

    def instance(self, options=None) -> Configg:
        return Configg(self.file_path(), XmlBackend, **options or {})

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(cls.file_path())

    def edit_file(self):
        with open(self.file_path(), "w+") as fp:
            fp.write("<config>"
                        "<section_one>"
                            "<val1>Stuff</val1>"
                            "<val2>apples</val2>"
                        "</section_one>"
                        "<section_two>"
                            "<val3>oranges</val3>"
                            "<val4>12</val4>"
                            "<val5>potato</val5>"
                        "</section_two>"
                    "</config>")

    @staticmethod
    def file_path():
        return "unittest.xml"

# Hack line to prevent unittest from trying to execute CommonTests (it has to be inherited first)
del(CommonTests)

if __name__ == "__main__":
    unittest.main()