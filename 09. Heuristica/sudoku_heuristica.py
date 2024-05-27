import heapq
import copy

class SudokuState:
    def __init__(self, board, moves=0, parent=None):
        self.board = board
        self.moves = moves
        self.parent = parent

    def __lt__(self, other):
        return self.f() < other.f()

    def f(self):
        return self.moves + self.heuristic()

    def heuristic(self):
        return sum(row.count(0) for row in self.board)

    def is_goal(self):
        return all(all(cell != 0 for cell in row) for row in self.board)

    def get_possible_values(self, row, col):
        if self.board[row][col] != 0:
            return []
        values = set(range(1, 10))
        values -= set(self.board[row])
        values -= {self.board[i][col] for i in range(9)}
        block_row, block_col = 3 * (row // 3), 3 * (col // 3)
        values -= {self.board[i][j] for i in range(block_row, block_row + 3) for j in range(block_col, block_col + 3)}
        return values

    def neighbors(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    for value in self.get_possible_values(row, col):
                        new_board = copy.deepcopy(self.board)
                        new_board[row][col] = value
                        yield SudokuState(new_board, self.moves + 1, self)
                    return

def solve_sudoku(start_board):
    start_state = SudokuState(start_board)
    frontier = []
    heapq.heappush(frontier, start_state)
    explored = set()

    while frontier:
        state = heapq.heappop(frontier)
        if state.is_goal():
            return state
        explored.add(tuple(tuple(row) for row in state.board))
        for neighbor in state.neighbors():
            neighbor_board = tuple(tuple(row) for row in neighbor.board)
            if neighbor_board not in explored:
                heapq.heappush(frontier, neighbor)
    return None

def print_solution(state):
    path = []
    while state:
        path.append(state.board)
        state = state.parent
    path.reverse()
    for board in path:
        for row in board:
            print(" ".join(str(cell) if cell != 0 else '.' for cell in row))
        print()

if __name__ == "__main__":
    start_board = [
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
    solution = solve_sudoku(start_board)
    if solution:
        print_solution(solution)
    else:
        print("No solution found.")