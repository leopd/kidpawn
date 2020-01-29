import random

import chess
from chess import Board, Move


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


def score_material_and_win(b:Board) -> int:
    if b.is_game_over():
        res = b.result()
        if res == '1/2-1/2':
            return 0
        elif res == '1-0':
            return 9999
        elif res == '0-1':
            return -9999
        else:
            raise RuntimeException(f"Unknown result {res}")
    else:
        return score_material(b)
    
def score_move(b:Board, m:Move, score_func) -> int:
    b.push(m)
    try:
        score = score_func(b)
        return score
    finally:
        b.pop()

def pick_move(b:Board, score_func=score_material_and_win, verbose:bool=False) -> Move:
    best_score = None
    best_moves = None
    def better(reference_score, new_score) -> bool:
        if reference_score is None:
            return True
        if b.turn == chess.WHITE:
            return new_score > reference_score
        else:
            return reference_score > new_score
    for move in b.legal_moves:
        score = score_move(b, move, score_func)
        if verbose:
            print(f"{move} gives {score}.")
        if better(best_score, score):
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    if verbose:
        print(f"\nBest moves are {best_moves} scoring {best_score}")
    return random.choice(best_moves)



def self_play(b:Board):

    while not b.is_game_over():
        m = pick_move(b)
        print(f"\nMaking move {m}")
        b.push(m)
        print(b)

    result = b.result()
    print("\n\nGame Over: {result}")
    return result

