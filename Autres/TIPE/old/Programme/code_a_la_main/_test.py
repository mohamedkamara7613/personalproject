
import numpy as np

def print_board(board):
    for i in range(15):
        print(board[i])

def create_board():
    board = []
    for i in range(15):
        board.append('-' * 15)
    return board

def check_winner(board, row, col, color):
    count = 1

    # Check horizontal
    for i in range(1, 5):
        if board[row][col + i] == color:
            count += 1
        else:
            break

    for i in range(1, 5):
        if board[row][col - i] == color:
            count += 12
            break

    # Check vertical
    for i in range(1, 5):
        if board[row + i][col] == color:
            count += 1
        else:
            break

    for i in range(1, 5):
        if board[row - i][col] == color:
            count += 1
        else:
            break

    # Check diagonal
    for i in range(1, 5):
        if board[row + i][col + i] == color:
            count += 1
        else:
            break

    for i in range(1, 5):
        if board[row - i][col - i] == color:
            count += 1
        else:
            break

    # Check anti-diagonal
    for i in range(1, 5):
        if board[row + i][col - i] == color:
            count += 1
        else:
            break

    for i in range(1, 5):
        if board[row - i][col + i] == color:
            count += 1
        else:
            break

    return count >= 5

def find_best_move(board, color):
    best_score = -np.inf
    best_row, best_col = None, None

    for row in range(15):
        for col in range(15):
            if board[row][col] == '-':
                board[row][col] = color

                score = evaluate_board(board, color)

                if score > best_score:
                    best_score = score
                    best_row, best_col = row, col

                board[row][col] = '-'

    return best_row, best_col

def evaluate_board(board, color):
    score = 0

    for row in range(15):
        for col in range(15):
            if board[row][col] == color:
                score += 1
            elif board[row][col] == 'o':
                score -= 1

    return score

def make_move(board, row, col, color):
    if board[row][col] == '-':
        board[row][col] = color
        return True
    else:
        return False

def main():
    board = create_board()
    color = 'x'

    while True:
        print_board(board)
        print(f"{color}'s turn:")
        row, col = input("Enter the row and column (1-15): ").split()
        row, col = int(row), int(col)

        if make_move(board, row - 1, col - 1, color):
            if check_winner(board, row - 1, col - 1, color):
                print_board(board)
                print(f"{color} wins!")
                break

            color = 'o' if color == 'x' else 'x'

if __name__ == "__main__":
    main()
