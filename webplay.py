from flask import Flask, request
app = Flask("kidpawn")

from kidpawn import Kidpawn

@app.route('/')
def display():
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
                Enter your move: <input name="move" />
                <input type="hidden" name="board" value="{board_fen}" />
                <input type="submit" value="Move" />
            </form>
    """
    if kp.game_over_msg():
        msg = kp.game_over_msg()
        form = ""
    return f"""
        <html>
            <h1>Kidpawn</h1>
            {board_svg}
            <br/>
            <h3>{msg}</h3>
            {form}
        </html>
    """

if __name__=='__main__':
    app.run()
