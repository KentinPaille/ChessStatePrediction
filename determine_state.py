import chess

def get_game_state(fen):
    board = chess.Board(fen)
    if board.is_checkmate():
        return "checkmate"
    elif board.is_stalemate():
        return "draw"
    elif board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        return "draw"
    elif board.is_check():
        return "check"
    else:
        return "ongoing"
