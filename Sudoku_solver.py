def solve(board):
	# Find an empty cell
	for i in range(9):
		for j in range(9):
			if board[i][j] == 0:
				# Try filling the empty cell with a number from 1 to 9
				for number in range(1, 10):
					if is_valid(board, i, j, number):
						# If the number is valid, fill the cell with it and try solving the rest of the puzzle
						board[i][j] = number
						if solve(board):
							return True
				# If no valid number was found, backtrack and try a different number
				board[i][j] = 0
				return False
	# If there are no empty cells, the puzzle is solved
	return True

def is_valid(board, row, col, number):
	# Check if the number is already in the row or column
	for i in range(9):
		if board[row][i] == number or board[i][col] == number:
			return False
	# Check if the number is already in the 3x3 block
	block_row = (row // 3) * 3
	block_col = (col // 3) * 3
	for i in range(3):
		for j in range(3):
			if board[block_row + i][block_col + j] == number:
				return False
	# If the number is not in the row, column, or block, it is valid
	return True

# Example usage:

board = [
	[5, 3, 0, 0, 7, 0, 0, 0, 0],
	[6, 0, 0, 1, 9, 5, 0, 0, 0],
	[0, 9, 8, 0, 0, 0, 0, 6, 0],
	[8, 0, 0, 0, 6, 0, 0, 0, 3],
	[4, 0, 0, 8, 0, 3, 0, 0, 1],
	[7, 0, 0, 0, 2, 0, 0, 0, 6],
	[0, 6, 0, 0, 0, 0, 2, 8, 0],
	[0, 0, 0, 4, 1, 9, 0, 0, 5],
	[0, 0, 0, 0, 8, 0, 0, 7, 9]
]

if solve(board):
	for row in board:
		print(row)
else:
	print("No solution found.")
