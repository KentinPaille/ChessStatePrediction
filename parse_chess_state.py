import numpy as np
from concurrent.futures import ProcessPoolExecutor

piece_map = {
    'p': 1, 'b': 2, 'n': 3, 'r': 4, 'q': 5, 'k': 6,
    'P': -1, 'B': -2, 'N': -3, 'R': -4, 'Q': -5, 'K': -6
}

def fen_to_array(fen: str) -> np.ndarray:
    board = []
    for row in fen.split()[0].split('/'):
        current_row = []
        for char in row:
            if char.isdigit():
                current_row.extend([0.0] * int(char))
            else:
                current_row.append(piece_map[char])
        board.append(current_row)
    return np.array(board, dtype=np.float32)

def batch_fens_to_arrays(fens: list[str]) -> np.ndarray:
    return np.stack([fen_to_array(fen) for fen in fens])

def parallel_batch_fens_to_arrays(fens: list[str], workers: int = 4) -> np.ndarray:
    with ProcessPoolExecutor(max_workers=workers) as executor:
        arrays = list(executor.map(fen_to_array, fens))
    return np.stack(arrays)

def print_board(board: np.ndarray):
    print("Current board state:")
    for row in board:
        print(' '.join(f"{int(x):2}" for x in row))
    print()

