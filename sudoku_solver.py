import random
import copy


def readSudoku(fileName, A):
    i = 0
    with open(fileName, 'r') as f:
        for line in f:
            line = line.strip()
            line = line.translate(None, '[] |-+')
            line = line.replace(".", "-1")
            line = line.replace(" ", ",")
            line = line.replace(",,", ",")
            # print "line #", i, line
            if len(line) > 0:
                A.append(map(int, line.split(',')))
                # B.append(map(int,line.split(',')))
                i += 1
    # print A


def writeSudoku(fileName, A):
    f = open(fileName, "w")
    for x in xrange(9):
        line = ""
        for y in xrange(9):
            if (A[x][y] == -1):
                # line += str(B[x][y]) + " "
                line += ". "
            else:
                line += str(A[x][y]) + " "
            if ((y + 1) % 3 == 0 and y != 8):
                line += "| "
        print line
        if ((x + 1) % 3 == 0 and x != 8):
            print "------+-------+------"


def numberOfDuplications(a):
    return 9 - len(set(a))


def errorSudoku(B):
    result = 0
    array = []

    # rows
    for x in xrange(9):
        array = B[x]
        result += numberOfDuplications(array)

    # columns
    for y in xrange(9):
        array = []
        for x in xrange(9):
            array.append(B[x][y])
        result += numberOfDuplications(array)

    # squares 3x3
    for i in xrange(3):
        for j in xrange(3):
            array = []
            for i1 in xrange(3):
                for j1 in xrange(3):
                    x = 3 * i + i1
                    y = 3 * j + j1
                    array.append(B[x][y])
            result += numberOfDuplications(array)
    return result


def errorSudoku2(B):
    result = 0
    array = 0

    # rows
    for x in xrange(9):
        for y in xrange(9):
            array += B[x][y];
        result += abs(array-45)

    # columns
    for y in xrange(9):
        array = 0
        for x in xrange(9):
            array += B[x][y]
        result += abs(array-45)

    # squares 3x3
    for i in xrange(3):
        for j in xrange(3):
            array = 0
            for i1 in xrange(3):
                for j1 in xrange(3):
                    x = 3 * i + i1
                    y = 3 * j + j1
                    array += B[x][y]
            result += abs(array-45)
    return result

# genetic algorithm
POPULATION_SIZE = 25
NUMBER_OF_GENERATIONS = 1000
NUMBER_OF_MUTATIONS = 1
MUTATION3_PROBABILITY = 0.1
STUCK_NUMBER = 100


def fillSudokuRandom(A):
    B = copy.deepcopy(A)
    for x in xrange(9):
        unused = list(set(range(1, 10)) - set(A[x]))
        random.shuffle(unused)
        for y in xrange(9):
            if (A[x][y] == -1):
                B[x][y] = unused.pop()
    return B


def crossoverSudoku(P1, P2):
    crossPoint = random.randint(1, len(P1))
    return copy.deepcopy(P1[:crossPoint] + P2[crossPoint:])


def mutationSudoku(pattern, A, _NUMBER_OF_MUTATIONS = NUMBER_OF_MUTATIONS):
    xId = range(9)
    random.shuffle(xId)
    for x in xId[:_NUMBER_OF_MUTATIONS]:
        swapAbleId = []
        for y in xrange(9):
            if (pattern[x][y] == -1):
                swapAbleId.append(y)
        if len(swapAbleId) >= 2:
            random.shuffle(swapAbleId)
            y1 = swapAbleId[0]
            y2 = swapAbleId[1]
            A[x][y1], A[x][y2] = A[x][y2], A[x][y1]


def mutationSudoku3(pattern, A, _NUMBER_OF_MUTATIONS = NUMBER_OF_MUTATIONS):
    xId = range(9)
    random.shuffle(xId)
    for x in xId[:_NUMBER_OF_MUTATIONS]:
        swapAbleId = []
        for y in xrange(9):
            if (pattern[x][y] == -1):
                swapAbleId.append(y)
        if len(swapAbleId) >= 3:
            random.shuffle(swapAbleId)
            y1 = swapAbleId[0]
            y2 = swapAbleId[1]
            y3 = swapAbleId[2]
            A[x][y1], A[x][y2], A[x][y3] = A[x][y2], A[x][y3], A[x][y1]

def solveSudoku(A):
    #random.seed(17239)
    # start population
    population = []
    for i in xrange(POPULATION_SIZE):
        B = fillSudokuRandom(A)
        population.append(list((errorSudoku(B), B)))

    lastBest = 100500
    # emulation of evolution
    for j in xrange(NUMBER_OF_GENERATIONS):
        # selection
        population.sort(key=lambda x: x[0])

        best = population[0][0]
        print best

        if best == lastBest:
            stuck += 1
        else:
            lastBest = best
            stuck = 0

        if stuck > STUCK_NUMBER:
            for i in range(1, POPULATION_SIZE):
                population[i][1] = fillSudokuRandom(A)
            stuck = 0

        # crossing + mutation
        for i in range(POPULATION_SIZE / 2):
            x = i
            y = POPULATION_SIZE - 1 - i
            # print x,y
            population[y][1] = crossoverSudoku(
                population[x][1], population[x + 1][1])
            if random.random() < MUTATION3_PROBABILITY:
                mutationSudoku3(A, population[y][1])
            else:
                mutationSudoku(A, population[y][1])

        # recalculate fitness function
        for i in xrange(POPULATION_SIZE):
            population[i][0] = errorSudoku(population[i][1])

    population.sort(key=lambda x: x[0])
    return copy.deepcopy(population[0][1])


if __name__ == '__main__':
    A = []
    readSudoku("input.txt", A)

    bestError = 100500
    for i in xrange(100):
        B = solveSudoku(A)
        error = errorSudoku(B)
        print "error = ", error
        if error < bestError:
            bestError = error
            C = B
            print "error = ", errorSudoku(C)
            writeSudoku("output.txt", C)

    writeSudoku("stdout", A)
    print "error = ", errorSudoku(C)
    writeSudoku("stdout", C)

"""
. 6 . | 4 . . | . . .
. . . | . . . | 9 . .
. . . | . . . | 3 4 8
------+-------+------
1 . . | . . 6 | . . 9
9 5 8 | 1 . . | . . .
. . . | 2 3 . | . . .
------+-------+------
6 . . | . . 4 | 2 3 .
. 4 . | . 2 . | . . 1
. 2 1 | . . . | 8 6 .
error =  0
8 6 3 | 4 9 5 | 7 1 2
7 1 4 | 3 8 2 | 9 5 6
2 9 5 | 7 6 1 | 3 4 8
------+-------+------
1 3 2 | 8 5 6 | 4 7 9
9 5 8 | 1 4 7 | 6 2 3
4 7 6 | 2 3 9 | 1 8 5
------+-------+------
6 8 9 | 5 1 4 | 2 3 7
3 4 7 | 6 2 8 | 5 9 1
5 2 1 | 9 7 3 | 8 6 4
"""
"""
. . 3 | . 2 . | 6 . .
9 . . | 3 . 5 | . . 1
. . 1 | 8 . 6 | 4 . .
------+-------+------
. . 8 | 1 . 2 | 9 . .
7 . . | . . . | . . 8
. . 6 | 7 . 8 | 2 . .
------+-------+------
. . 2 | 6 . 9 | 5 . .
8 . . | 2 . 3 | . . 9
. . 5 | . 1 . | 3 . .
error =  0
4 8 3 | 9 2 1 | 6 5 7
9 6 7 | 3 4 5 | 8 2 1
2 5 1 | 8 7 6 | 4 9 3
------+-------+------
5 4 8 | 1 3 2 | 9 7 6
7 2 9 | 5 6 4 | 1 3 8
1 3 6 | 7 9 8 | 2 4 5
------+-------+------
3 7 2 | 6 8 9 | 5 1 4
8 1 4 | 2 5 3 | 7 6 9
6 9 5 | 4 1 7 | 3 8 2
"""
