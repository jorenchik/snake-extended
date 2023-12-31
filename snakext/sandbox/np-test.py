import numpy as np

column_count = 5
row_count = 5

LOCAL_SNAKE_HEAD = "h1"
LOCAL_SNAKE_BODY = "b1"
LOCAL_SNAKE_TAIL = "t1"

REMOTE_SNAKE_HEAD = "h2"
REMOTE_SNAKE_BODY = "b2"
REMOTE_SNAKE_TAIL = "t2"

WALL = "w"
FOOD = "f"
POISON = "p"
VOID = "v"

constants = [
    LOCAL_SNAKE_HEAD, LOCAL_SNAKE_BODY, LOCAL_SNAKE_TAIL, REMOTE_SNAKE_HEAD,
    REMOTE_SNAKE_BODY, REMOTE_SNAKE_TAIL, WALL, FOOD, POISON
]


def check_sum_duplicates(strings: list[str]) -> bool:
    resulting_sums = []
    duplicates = []
    for i in range(0, len(constants) - 1):
        for k in range(i, len(constants) - 1):
            sum = constants[i] + constants[k + 1]
            print(constants[i], constants[k + 1], sum, sep=' and ')
            if sum not in resulting_sums:
                resulting_sums.append(sum)
            else:
                duplicates.append(sum)
    return len(duplicates) > 0


arr = np.array([VOID for x in range(0, column_count * row_count)
                ]).reshape(row_count, column_count)

arr_2 = np.array([VOID for x in range(0, column_count * row_count)
                  ]).reshape(row_count, column_count)

print(np.char.add(arr, arr_2))
