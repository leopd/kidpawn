import random
import traceback

import chess
from chess import Board, Move

class HEURISTIC:
    PAWN_PROMOTION = 4.3


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


def _pawn_distance_to_promote(position:int, color:bool):
    """Returns the number of moves this pawn must make before it 
    gets promoted.  Position is an int 0-63, and color is chess.WHITE or chess.BLACK
    """
    assert position in range(64)
    rank = (position // 8) + 1  # 1-8
    if color == chess.WHITE:
        return 8-rank
    else:
        return rank

def pawn_position_bonus(b:Board) -> float:
    """Returns white - black advantage just for pawn position.
    """
    total = 0
    for color, sign in [(chess.WHITE, 1), (chess.BLACK, -1)]:
        for pawn in b.pieces(chess.PAWN, color):
            dist = _pawn_distance_to_promote(pawn, sign)
            total += sign * HEURISTIC.PAWN_PROMOTION / dist
    return total


def score_material_and_win(b:Board) -> int:
    if b.can_claim_draw():
        return 0
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

def score_board(b:Board) -> float:
    """Returns a score for the board.
    Uses the board's own score function (my_score) if monkey-patched in,
    else uses score_material_and_win by default
    """
    if hasattr(b,'my_score'):
        return b.my_score()
    else:
        return score_material_and_win(b)


def score_move(b:Board, m:Move) -> float:
    b.push(m)
    try:
        score = score_board(b)
        return score
    finally:
        b.pop()

def pick_move(b:Board, verbose:bool=False) -> Move:
    """Enumerate all valid moves, and pick the one most advantageous to the current player
    """
    best_score = None
    best_moves = None
    def is_better(reference_score, new_score) -> bool:
        if reference_score is None:
            return True
        if b.turn == chess.WHITE:
            return new_score > reference_score
        else:
            return reference_score > new_score
    for move in b.legal_moves:
        score = score_move(b, move)
        if verbose:
            print(f"{move} gives {score}.")
        if is_better(best_score, score):
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    if verbose:
        print(f"\nBest moves are {best_moves} scoring {best_score}")
    return random.choice(best_moves)


def lookahead1_move(original:Board, verbose:bool=False) -> Move:
    """Looks ahead one move
    """
    best_score = None
    best_moves = None
    def is_better(reference_score, new_score) -> bool:
        if reference_score is None:
            return True
        if original.turn == chess.WHITE:
            return new_score > reference_score
        else:
            return reference_score > new_score
    my_moves = list(original.legal_moves)
    for my_move in my_moves:
        b = original.copy()
        b.push(my_move)
        if b.is_game_over():
            score = score_board(b)
        else:
            their_move = pick_move(b)
            b.push(their_move)
            score = score_board(b)
        if verbose:
            print(f"{my_move} then {their_move} gives {score}.")
        if is_better(best_score, score):
            best_score = score
            best_moves = [my_move]
        elif score == best_score:
            best_moves.append(my_move)

    if verbose:
        print(f"\nBest moves are {best_moves} scoring {best_score}")
    if best_moves:
        return random.choice(best_moves)
    else:
        print("No valid moves to pick from")
        return None

def self_play(b:Board):

    while not b.is_game_over():
        if b.can_claim_draw():
            print("Draw")
            break
        m = pick_move(b)
        print(f"\nMaking move {m}")
        b.push(m)
        print(b)

    result = b.result()
    print(f"\n\nGame Over: {result}")
    return result, b


class Kidpawn():

    def __init__(self, board_fen:str=None):
        if board_fen:
            self.b = Board(board_fen)
        else:
            # Not sure why this is needed.
            self.b = Board()

    def svg(self):
        return self.b._repr_svg_()

    def fen(self):
        """Returns board state as a FEN string
        """
        return self.b.fen()

    def move(self, move:str) -> [bool, str]:
        """Returns true if the move succeeded
        """
        try:
            self.b.push_uci(move)
            return True, "ok"
        except ValueError as e:
            msg = str(e)
            if msg.startswith("illegal uci"):
                return False, f"illegal move: {move}.  Try something like d2d4 or h7h8q."
            else:
                return False, f"other error {msg}"
        except Exception as e:
            traceback.print_exc()
            return False, f"unknown error {e}"

    def bot_move(self):
        """Computer makes a move herself, and updates the board
        """
        m = lookahead1_move(self.b)
        if m:
            return self.move(m.uci())
        else:
            return False, "No valid moves"

    def game_over_msg(self) -> str:
        """If the game is over, returns a string why.
        If game is not over, return blank
        """
        if self.b.is_game_over():
            return f"Game over: {self.b.result()}"
        else:
            return None

