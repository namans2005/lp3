n = 8

def n_queens(n, row=1, columns=[0], diagonal1=[0], diagonal2=[0]):
    if row == n:
        for col in columns:
            print([int(i == col) for i in range(n)])
        return True

    for col in range(n):
        if (col not in columns and
            row-col not in diagonal1 and
            row+col not in diagonal2):

            if n_queens(n, row+1,
                        columns+[col],
                        diagonal1+[row-col],
                        diagonal2+[row+col]):
                return True

    return False

n_queens(n)