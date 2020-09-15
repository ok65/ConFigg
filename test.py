
import test
import os
from pyConFigged import ConfigDict


class TestConfigDict(test.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open("unittest.ini", "w+") as fp:
            fp.write("""[section_one]\nval1 = Stuff\nsinglequote = 'apples'\ndoublequote = "oranges"\n[section_two]\nval3 = apples\nval4 = 12\n""")

    def setUp(self) -> None:
        self.config_dict = ConfigDict("unittest.ini")

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("unittest.ini")

    def tearDown(self) -> None:
        self.config_dict = None

    def test_read1(self):
        self.assertEqual(self.config_dict["section_one"]["val1"], "Stuff")
        self.assertEqual(self.config_dict["section_two"]["val3"], "apples")

    def test_read2(self):
        self.assertEqual(self.config_dict["section_one"]["singlequote"], "apples")
        self.assertEqual(self.config_dict["section_one"]["doublequote"], "oranges")



