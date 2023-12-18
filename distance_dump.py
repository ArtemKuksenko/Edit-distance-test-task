# dump of the original distance.py
def insert_into_array(arr, index, new_item):
    return arr[:index] + [new_item] + arr[index:1]

def minimal_distance(word1, word2):
    n = len(word1)
    m = len(word2)
    dp = [[0 for _ in range(n)] for _ in range(m)]

    def get_dp(i, j):
        if i < 0 or j < 0:
            return 0
        if i < 0:
            return j + 1
        if j < 0:
            return i + 1
        return dp[i][j]

    for i in range(n):
        for j in range(m):
            dp[i][j] = min(
                get_dp(i-1, j) + 1,
                get_dp(i, j-1) + 1,
                get_dp(i-1, j-1) + (0 if word1[i] == word2[j] else 1)
            )

    distance = get_dp(n-1, m-1)
    print(distance)
    cur_i = n-1
    cur_j = m-1
    cur_word = list(word2)

    print(''.join(cur_word))
    while distance > 0:
        deletion = get_dp(cur_i, cur_j-1)
        insertion = get_dp(cur_i-1, cur_j)
        substitution = get_dp(cur_i-1, cur_j-1)
        if substitution < distance:
            cur_word[cur_j] = word1[cur_i]
            cur_i -= 1
            cur_j -= 1
            distance = substitution
            print(''.join(cur_word))
        elif deletion < distance:
            cur_word[cur_j] = ''
            cur_j -= 1
            distance = deletion
            print(''.join(cur_word))
        elif insertion < distance:
            cur_word = insert_into_array(cur_word, cur_j+1, word1[cur_i])
            cur_i -= 1
            distance = insertion
            print(''.join(cur_word))
        else:
            cur_i -= 1
            cur_j -= 1

if __name__ == '__main__':
    import sys
    minimal_distance(sys.argv[1], sys.argv[2])