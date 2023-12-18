import sys

from words_transformation import WordsTransformation


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python distance.py word1 word2")
        raise ValueError("incorrect number of arguments")
    wt = WordsTransformation(sys.argv[1], sys.argv[2])
    print(wt.get_minimal_distance())
    for step in wt.get_transformation():
        print(step)
