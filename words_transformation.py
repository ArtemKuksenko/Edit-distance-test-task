from collections import namedtuple
from typing import Generator

UNDEFINED = -1  # negative int constant

# actions cost
INSERT_COST = 1
DELETE_COST = 1
REPLACE_COST = 1


Action = namedtuple(
    'Action',
    'deletion insertion substitution skip',
    defaults=(UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED)
)


class WordsTransformation:
    def __init__(self, word1: str, word2: str):
        self.word1, self.word2 = word1, word2

        self._cache: list[list[int]] = [
            [UNDEFINED for _ in range(len(word2))]
            for _ in range(len(word1))
        ]

    def _get_min_distance(self, i: int, j: int) -> int:
        """
        Calculate the distance of transformation from word1[:i+1] to word2[:j+1]
        """
        if i < 0 and j < 0:
            # no Actions
            return 0

        if i < 0:
            # word2[:j+1] have j + 1 symbols and word1[:i] is empty.
            # we need to add the j + 1 symbols from the word2 to word1 to make them equal (
            #   word1[:j+1]== word2[:j+1]
            # ).
            # Count of steps is j + 1
            return (j + 1) * INSERT_COST
        if j < 0:
            # word1[:i+1] have i + 1 symbols and word[:j] is empty.
            # we need to drop the i + 1 symbols from the word1 to make them equal ("" == "").
            # Count of steps is i + 1
            return (i + 1) * DELETE_COST

        if self._cache[i][j] != UNDEFINED:
            return self._cache[i][j]

        self._cache[i][j] = min(
            # action: drop one symbol from word1:
            self._get_min_distance(i - 1, j) + DELETE_COST,
            # action: add one symbol from word2 to word1:
            self._get_min_distance(i, j - 1) + INSERT_COST,
            # action: swap one symbol from word2 to word1 if they are not equal:
            self._get_min_distance(i - 1, j - 1) + (0 if self.word1[i] == self.word2[j] else REPLACE_COST)
        )
        return self._cache[i][j]

    def get_minimal_distance(self) -> int:
        return self._get_min_distance(len(self.word1) - 1, len(self.word2) - 1)

    @staticmethod
    def _insert_into_array(arr: list[str], index: int, new_item: str) -> list[str]:
        return arr[:index] + [new_item] + arr[index:]

    def get_transformation(self) -> Generator[str, None, None]:
        yield self.word1

        cur_i, cur_j = len(self.word1) - 1, len(self.word2) - 1

        distance = self.get_minimal_distance()

        cur_word = list(self.word1)

        while distance > 0:
            if cur_i < 0:
                a = Action(insertion=distance)
            elif cur_j < 0:
                a = Action(deletion=distance)
            else:
                a = Action(
                    deletion=self._get_min_distance(cur_i - 1, cur_j) + INSERT_COST,
                    insertion=self._get_min_distance(cur_i, cur_j - 1) + DELETE_COST,
                    substitution=(
                        0 if self.word1[cur_i] == self.word2[cur_j]
                        else self._get_min_distance(cur_i - 1, cur_j - 1) + REPLACE_COST
                    ),
                    skip=(
                        0 if self.word1[cur_i] != self.word2[cur_j]
                        else self._get_min_distance(cur_i - 1, cur_j - 1)
                    )
                )
            match distance:
                case a.skip:
                    cur_i -= 1
                    cur_j -= 1
                case a.substitution:
                    cur_word[cur_i] = self.word2[cur_j]
                    distance -= REPLACE_COST
                    yield ''.join(cur_word)
                    cur_i -= 1
                    cur_j -= 1
                case a.deletion:
                    cur_word[cur_i] = ''
                    cur_i -= 1
                    distance -= DELETE_COST
                    yield ''.join(cur_word)
                case a.insertion:
                    cur_word = self._insert_into_array(cur_word, cur_i + 1, self.word2[cur_j])
                    cur_j -= 1
                    yield ''.join(cur_word)
                    distance -= INSERT_COST
                case _:
                    raise ValueError("Incorrect distance")
