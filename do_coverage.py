
import coverage
import unittest
import sys

cov = coverage.Coverage()
cov.start()
import test
unittest.main(exit=False, )
cov.stop()
cov.save()
sys.exit("{}%".format(int(cov.report())))