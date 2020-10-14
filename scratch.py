
from configg import Configg

if __name__ == "__main__":

    cd = Configg("test.ini")

    fp = open("test.ini", "w+")

    cd.section_one["val1"] = "new"

    fp.close()

    pass