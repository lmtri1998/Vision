import os
from utils import StringDistance, extract_digit


class GenderCorrection:
    """Correct Religion based on input by comparing Levenshtein distance to
    tongiao.txt
    """

    def __init__(self, cost_dict_path=None, gender_path = None):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        if cost_dict_path is None:
            cost_dict_path = os.path.join(dir_path, 'data', 'cost_char_dict.txt')
        if gender_path is None:
            gender_path = os.path.join(dir_path, 'data', 'gioitinh.txt')
        self.string_distance = StringDistance(cost_dict_path=cost_dict_path)
        self.genders = []
        with open(gender_path, 'r', encoding='utf-8') as f:
            for line in f:
                entity = line.strip()
                if not entity:
                    break
                entity = entity.split('\n')
                self.genders.extend(entity)
        self.genders = tuple(set(self.genders))


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

    def gender_correction(self, gender):
        if not isinstance(gender, str):
            raise ValueError("Only Str Input")
        gender = gender.replace('.', ' ')
        result = self.correct(gender, self.genders, nb_candidates=1, distance_threshold=20)
        if len(result) != 0:
            return result[0][0], result[0][1]
        else:
            return gender, -1


if __name__ == '__main__':
    a = GenderCorrection()
    print(a.gender_correction("nú"))
