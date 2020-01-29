import chess
from chess import Board, Move


def score_move(b:Board, m:Move) -> int:
    b.push(m)
    s = score_material(b)
    b.pop()
    return s

def score_material(b:Board) -> int:
    """Returns sum(white) - sum(black)
    """
    strengths = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 10,
    }
    total = 0
    for piece_type, value in strengths.items():
        for color, sign in [(chess.WHITE, 1), (chess.BLACK, -1)]:
            p = b.pieces(piece_type, color)
            num_p = len(p)
            total += sign * num_p * strengths[piece_type]
    return total
    

def consider_moves(b:Board, score_func=score_move) -> Move:
    best_score = None
    best_moves = None
    for move in b.legal_moves:
        score = score_func(b, move)
        print(f"considering {move} gives {score}")
        if (best_score is None) or (score > best_score):
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)
    return best_moves

