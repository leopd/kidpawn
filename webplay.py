import random
import time

from flask import Flask, request
app = Flask("kidpawn")

from kidpawn import Kidpawn

@app.route('/')
def display():
    random.seed(int(time.time() / 1000))  # slow-moving seed so reload doesn't get you a better move
    old_fen = request.args.get('board')
    move = request.args.get('move')
    kp = Kidpawn(old_fen)

    if move:
        success, msg = kp.move(move)
        if success:
            #TODO: show them their own move first somehow.  javascript or something.
            kp.self_play()
    else:
        msg = "your turn"
    board_svg = kp.svg()
    board_fen = kp.fen()
    form = f"""
        <form>
            Enter your move: 
            <input name="move" type="text" placeholder="like d2d4 or h7h8q" 
                autofocus="autofocus"
                />
            <input type="hidden" name="board" value="{board_fen}" />
            <input type="submit" value="Move" />
        </form>
    """
    if kp.game_over_msg():
        msg = kp.game_over_msg()
        form = """
            <a href="/">New Game</a>
        """

    return f"""
        <html>
            {board_svg}
            <br/>
            <h3>{msg}</h3>
            {form}
        </html>
    """

if __name__=='__main__':
    app.run(host='0.0.0.0')
