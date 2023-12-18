# Edit distance test task

## The task:
The code in this project measures edit distance between two words:

_Given two words word1 and word2, calculates the minimum number of operations required to convert word1 to word2.
You have the following 3 operations permitted on a word:
Insert a character
Delete a character
Replace a character_

How to run:
python distance.py word1 word2

Your task is to spot any mistakes in the code, improve its readability and highlight any performance issues if any.

Here is a list of points:
- Look at the current algorithm implementation and propose a way(s) to improve it (no coding needed here)
- Refactor code (feel free to change anything)
- Add tests. For testing purposes you can add any testing library you want.

## Implementation:
- Original **distance.py** file is [here](https://github.com/ArtemKuksenko/Edit-distance-test-task/blob/main/distance_dump.py)
- Install [requirements](https://github.com/ArtemKuksenko/Edit-distance-test-task/blob/main/requirements_dev.txt):
  _(include pytest, mypy, flake8)_ 
  ```
  python3.11 -m pip install -r requirements_dev.txt
  ```
- Run flake8 linter:
  ```
  flake8 .
  ```
- Run mypy linter:
  ```
  mypy .
  ```
- Run unit tests:
  ```
  coverage run -m pytest -v -s
  coverage report -m
  ```
- Run application:
  ```
  python3.11 distance.py word1 word2
  ```
