from unittest import TestSuite
import unittest
import os
class SilverEngineTestSuite(object):

    @staticmethod
    def run():
        modules_to_test = []
        test_dir = os.listdir('.')
        for test in test_dir:
            if test.startswith('Test') and test.endswith('.py'):
                modules_to_test.append(test.rstrip('.py'))

        suite = TestSuite()
        for module in map(__import__, modules_to_test):
            suite.addTest(unittest.findTestCases(module))
        return suite # unittest.main(defaultTest='suite')


if __name__ == '__main__':
    unittest.main(defaultTest= 'SilverEngineTestSuite.run')