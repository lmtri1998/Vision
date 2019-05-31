import os
from collections import defaultdict
from String_distance import StringDistance, extract_digit

class ReligionCorrection:
    """Correct Religion based on input by comparing Levenshtein distance to
    tongiao.txt
    """

    def __init__(self, cost_dict_path=None, religion_path=None):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        if cost_dict_path is None:
            cost_dict_path = os.path.join(dir_path, 'data', 'cost_char_dict.txt')
        if religion_path is None:
            religion_path = os.path.join(dir_path, 'data', 'tongiao.txt')
        self.string_distance = StringDistance(cost_dict_path=cost_dict_path)
        self.religions = []
        with open(religion_path, 'r', encoding='utf-8') as f:
            for line in f:
                entity = line.strip()
                if not entity:
                    break
                entity = entity.split('\n')
                self.religions.extend(entity)
            print(self.religions)
        self.religions = tuple(set(self.religions))

    def correct(self, phrase, correct_phrases, nb_candidates=2, distance_threshold=40):
        candidates = [(None, distance_threshold)] * nb_candidates
        max_diff_length = distance_threshold
        for correct_phrase in correct_phrases:
            if abs(len(phrase) - len(correct_phrase)) >= max_diff_length:
                continue
            if extract_digit(correct_phrase) != extract_digit(phrase):
                distance = 100
            else:
                distance = self.string_distance.distance(phrase, correct_phrase)
            if distance < candidates[-1][1]:
                candidates[-1] = (correct_phrase, distance)
                candidates.sort(key=lambda x: x[1])
        return candidates

    def _religion_correction(self, tokens):
        result_distance = 1000
        result = None
        nb_of_tokens = len(tokens)
        early_stop_threshold = 0
        stop_correction = False
        for index_province in range(max(0, nb_of_tokens - 4), nb_of_tokens):
            phrase = ' '.join(tokens[index_province:])
            province_candidates = self.correct(phrase, self.provinces)
            for province, distance_province in province_candidates:
                if distance_province > result_distance or province is None:
                    continue
                result_candidate, result_distance_candidate = self._district_correction(
                    tokens, '', province, index_province,
                    distance_province, result_distance
                )
                if result_distance_candidate < result_distance:
                    result_distance = result_distance_candidate
                    result = result_candidate
                if index_province > 0:
                    if tokens[index_province-1] in ['tp', 't/p']:
                        if index_province <= 1:
                            result = 'tp ' + province
                            result_distance = distance_province
                            continue
                        result_candidate, result_distance_candidate = self._district_correction(
                            tokens, 'tp', province, index_province - 1,
                            distance_province, result_distance
                        )
                        if result_distance_candidate < result_distance:
                            result_distance = result_distance_candidate
                            result = result_candidate
                    elif tokens[index_province].startswith('tp'):
                        if index_province <= 1:
                            result = 'tp ' + province
                            result_distance = distance_province
                            continue
                        result_candidate, result_distance_candidate = self._district_correction(
                            tokens, 'tp', province, index_province,
                            distance_province, result_distance
                        )
                        if result_distance_candidate < result_distance:
                            result_distance = result_distance_candidate
                    elif self.string_distance.distance(tokens[index_province-1], 'tỉnh') < 10:
                        if index_province <= 1:
                            result = 'tỉnh ' + province
                            result_distance = distance_province
                            continue
                        result_candidate, result_distance_candidate = self._district_correction(
                            tokens, 'tỉnh', province, index_province-1,
                            distance_province, result_distance
                        )
                        if result_distance_candidate < result_distance:
                            result_distance = result_distance_candidate
                            result = result_candidate
                    elif index_province > 1 and self.string_distance.distance(' '.join(tokens[index_province-2:index_province]), 'thành phố') < 20:
                        if index_province <= 1:
                            result = 'thành phố ' + province
                            result_distance = distance_province
                            continue
                        result_candidate, result_distance_candidate = self._district_correction(
                            tokens, 'thành phố', province, index_province-2,
                            distance_province, result_distance
                        )
                        if result_distance_candidate < result_distance:
                            result_distance = result_distance_candidate
                            result = result_candidate
                if index_province <= 0:
                    if distance_province < result_distance:
                        result_distance = distance_province
                        result = province
                if distance_province <= early_stop_threshold:
                    stop_correction = True
                    break
            if stop_correction:
                break
        return result, result_distance


if __name__ == '__main__':
   r = ReligionCorrection()

