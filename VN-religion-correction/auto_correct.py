import os
from collections import defaultdict
from String_distance import StringDistance, extract_digit

class ReligionCorrection:
    """Correct Religion based on input by comparing Levenshtein distance to
    tongiao.txt
    """

    def __init__(self, cost_dict_path = None, religion_dict_path = None):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        if cost_dict_path is None:
            cost_dict_path = os.path.join(dir_path, 'data', 'cost_char_dict.txt')
        if religion_dict_path is None:
            religion_dict_path = os.path.join(dir_path, 'data', 'tongiao.txt')
