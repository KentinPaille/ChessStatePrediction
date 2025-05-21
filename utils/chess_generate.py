import chess
import pandas as pd
import random

def random_legal_position(check=False, checkmate=False, draw=False):
    board = chess.Board()
    max_plies = 80

    for _ in range(100):
        board = chess.Board()
        plies = random.randint(10, max_plies)
        for _ in range(plies):
            if board.is_game_over():
                break
            moves = list(board.legal_moves)
            move = random.choice(moves)
            board.push(move)

        if check and board.is_check() and not board.is_checkmate():
            return board.fen()
        elif checkmate and board.is_checkmate():
            return board.fen()
        elif draw and (board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition()):
            return board.fen()
        elif not check and not checkmate and not draw:
            if not board.is_check() and not board.is_checkmate() and not board.is_stalemate() and not board.is_insufficient_material() and not board.is_seventyfive_moves() and not board.is_fivefold_repetition():
                return board.fen()
    return None

def generate_dataset(n_ongoing=5, n_check=5, n_checkmate=5, n_draw=5):
    fens = []
    labels = []
    for _ in range(n_ongoing):
        fen = random_legal_position()
        if fen:
            fens.append(fen)
            labels.append('ongoing')
    for _ in range(n_check):
        fen = random_legal_position(check=True)
        if fen:
            fens.append(fen)
            labels.append('check')
    for _ in range(n_checkmate):
        fen = random_legal_position(checkmate=True)
        if fen:
            fens.append(fen)
            labels.append('checkmate')
    for _ in range(n_draw):
        fen = random_legal_position(draw=True)
        if fen:
            fens.append(fen)
            labels.append('draw')
    return pd.DataFrame({'FEN': fens, 'State': labels})

if __name__ == "__main__":
    df = generate_dataset(n_ongoing=5, n_check=5, n_checkmate=5, n_draw=5)
    print(df['State'].value_counts())
    print(df.head())
    df.to_csv("custom_chess_states.csv", index=False)
    print("Dataset généré et sauvegardé sous custom_chess_states.csv")
