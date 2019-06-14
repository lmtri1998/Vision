import os
import unittest
from gender_correction import GenderCorrection


class ReligionCorrectionTest(unittest.TestCase):
    def setUp(self):
        self.gen_corr = GenderCorrection()

    def test_address_correction(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, 'gender_test.txt'), encoding='utf-8') as f:
            for line in f:
                wrong_gender, gt_gender = line.split('|')
                wrong_gender = wrong_gender.strip().lower()
                gt_gender = gt_gender.strip()
                result = self.gen_corr.gender_correction(wrong_gender)
                corrected_gender = result[0]
                print(gt_gender)
                self.assertEqual(corrected_gender, gt_gender)


if __name__ == '__main__':
    unittest.main()

