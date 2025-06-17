import numpy as np
from concurrent.futures import ProcessPoolExecutor

piece_map = {
    'p': 1, 'b': 2, 'n': 3, 'r': 4, 'q': 5, 'k': 6,
    'P': -1, 'B': -2, 'N': -3, 'R': -4, 'Q': -5, 'K': -6
}

def fen_to_onehot(fen):
    piece_list = ['p', 'n', 'b', 'r', 'q', 'k', 'P', 'N', 'B', 'R', 'Q', 'K']
    piece_to_idx = {p: i for i, p in enumerate(piece_list)}
    board, *_ = fen.split()
    rows = board.split('/')
    onehot = np.zeros((8, 8, 13), dtype=np.int8)
    for i, row in enumerate(rows):
        col = 0
        for char in row:
            if char.isdigit():
                col += int(char)
            else:
                idx = piece_to_idx[char]
                onehot[i, col, idx] = 1
                col += 1
    return onehot

def batch_fens_to_arrays(fens: list[str]) -> np.ndarray:
    return np.stack([fen_to_onehot(fen) for fen in fens])

def parallel_batch_fens_to_arrays(fens: list[str], workers: int = 4) -> np.ndarray:
    with ProcessPoolExecutor(max_workers=workers) as executor:
        arrays = list(executor.map(fen_to_onehot, fens))
    return np.stack(arrays)

def print_board(board: np.ndarray):
    print("Current board state:")
    for row in board:
        print(' '.join(f"{int(x):2}" for x in row))
    print()

