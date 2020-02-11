import pytest

import kidpawn
from chess import Board

def test_score():
    b = Board()
    assert kidpawn.score_board(b) == 0

def _kp_sane(kp:kidpawn.Kidpawn):
    svg = kp.svg()
    assert isinstance(svg, str)
    assert len(svg) > 100

    fen = kp.fen()
    assert isinstance(fen, str)
    assert len(fen) > 10
    assert len(fen) < 200

    
def test_selfplay():
    kp = kidpawn.Kidpawn()
    _kp_sane(kp)

    for games in range(2):
        for moves in range(7):
            kp.bot_move()
            _kp_sane(kp)
