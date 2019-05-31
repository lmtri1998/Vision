import os
import unittest
from auto_correct import ReligionCorrection


class ReligionCorrectionTest(unittest.TestCase):
    def setUp(self):
        self.rel_corr = ReligionCorrection()

    def test_address_correction(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, 'religion_test.txt'), encoding='utf-8') as f:
            for line in f:
                wrong_religion, gt_religion = line.split('|')
                wrong_religion = wrong_religion.strip().lower()
                gt_religion = gt_religion.strip()
                result = self.rel_corr.religion_correction(wrong_religion)
                corrected_religion = result[0]
                print(gt_religion)
                self.assertEqual(corrected_religion, gt_religion)


if __name__ == '__main__':
    unittest.main()

