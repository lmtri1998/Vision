import os
import unittest
from ethnic_correction import EthnicCorrection


class EthnicCorrectionTest(unittest.TestCase):
    def setUp(self):
        self.eth_corr = EthnicCorrection()

    def test_address_correction(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, 'ethnic_test.txt'), encoding='utf-8') as f:
            for line in f:
                wrong_ethnic, gt_ethnic = line.split('|')
                wrong_ethnic = wrong_ethnic.strip().lower()
                gt_ethnic = gt_ethnic.strip()
                result = self.eth_corr.ethnic_correction(wrong_ethnic)
                corrected_ethnic = result[0]
                self.assertEqual(corrected_ethnic, gt_ethnic)


if __name__ == '__main__':
    unittest.main()

