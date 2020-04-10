import unittest
import FaultLocalization
import copy
import TestCaseReduction

class MyTestCase(unittest.TestCase):
    """
        测试用例集
    """

    def test_02_Mutants_statementSet(self):
        mutants = {1: [114, 1, '(', '(!'], 2: [130, 0, '=', '=='], 3: [130, 0, '=', '!='], 4: [130, 0, '=', '<']}
        mutant = FaultLocalization.Mutants()
        result = mutant.statementSet(mutants=mutants)
        exceptResult = [114]
        self.assertEqual(first=result, second=exceptResult)

    def test_03_Mutants_statementSet(self):
        mutants = {}
        mutant = FaultLocalization.Mutants()
        result = mutant.statementSet(mutants=mutants)
        exceptResult = []
        self.assertEqual(first=result, second=exceptResult)

    def test_06_MBFL_rankTable(self):
        case = FaultLocalization.MBFL()
        case.suspiciousnessTable = copy.deepcopy({1: 0.7, 2: 0.7, 3: 0.7, 4: 0.7, 5: 0.3, 6: 0.3})
        result = case.rankTable(faultPosition=3)
        exceptResult = [0.4167, 2.5]
        self.assertEqual(first=result, second=exceptResult)


if __name__ == '__main__':
    unittest.main()
