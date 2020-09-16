
import unittest
import os
from configg import Configg
from configg.ini_backend import IniBackend
from configg.json_backend import JsonBackend
from configg.xml_backend import XmlBackend


class CommonTests(unittest.TestCase):
    config_dict = None
    config_data = {"section_one": {"val1": "Stuff", "val2": "apples"},
                   "section_two": {"val3": "oranges", "val4": 12} }

    def edit_file(self):
        raise NotImplemented

    def instance(self):
        raise NotImplemented

    def setUp(self) -> None:
        self.config_dict = self.instance()

    def tearDown(self) -> None:
        self.config_dict = None

    def test_read1(self):
        self.assertEqual(self.config_dict.section_one["val1"], "Stuff")
        self.assertEqual(self.config_dict.section_one["val2"], "apples")
        self.assertEqual(self.config_dict.section_two["val3"], "oranges")

    def test_write1(self):
        self.config_dict.section_one["new_entry"] = "new value"
        self.config_dict.commit()
        cd2 = self.instance()
        self.assertEqual(cd2.section_one["new_entry"], "new value")

    def test_add_section(self):
        self.config_dict.add_section("new_section", {"bird": "duck"})
        self.assertEqual(self.config_dict.new_section["bird"], "duck")

    def test_reload(self):
        self.edit_file()
        self.assertNotIn("val5", self.config_dict.section_two)
        self.config_dict.reload()
        self.assertEqual(self.config_dict.section_two["val5"], "potato")


class IniTests(CommonTests):

    @classmethod
    def setUpClass(cls) -> None:
        with open("unittest.ini", "w+") as fp:
            fp.write("[section_one] \n"
                     "val1 = Stuff \n"
                     "val2 = apples \n"
                     "[section_two] \n"
                     "val3 = oranges \n"
                     "val4 = 12 ")

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("unittest.ini")

    def instance(self) -> Configg:
        return Configg("unittest.ini", data_backend=IniBackend)

    def edit_file(self):
        with open("unittest.ini", "a+") as fp:
            fp.write("""\nval5 = potato""")


class JsonTests(CommonTests):

    @classmethod
    def setUpClass(cls) -> None:
        with open("unittest.json", "w+") as fp:
            fp.write("""{"section_one": {"val1": "Stuff",
                                         "val2": "apples"},
                         "section_two": {"val3": "oranges",
                                         "val4": 12}}""")

    def instance(self) -> Configg:
        return Configg("unittest.json", data_backend=JsonBackend)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("unittest.json")

    def edit_file(self):
        with open("unittest.json", "w+") as fp:
            fp.write("""{"section_one": {"val1": "Stuff",
                                         "val2": "apples"},
                         "section_two": {"val3": "oranges",
                                         "val4": 12,
                                         "val5": "potato"}}""")

class XmlTests(CommonTests):

    @classmethod
    def setUpClass(cls) -> None:
        with open("unittest.xml", "w+") as fp:
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

    def instance(self) -> Configg:
        return Configg("unittest.xml", XmlBackend)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("unittest.xml")

    def edit_file(self):
        with open("unittest.xml", "w+") as fp:
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

# Hack line to prevent unittest from trying to execute CommonTests (it has to be inherited first)
del(CommonTests)

if __name__ == "__main__":
    unittest.main()