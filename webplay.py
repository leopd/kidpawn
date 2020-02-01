from flask import Flask, request
app = Flask("kidpawn")

from kidpawn import Kidpawn

@app.route('/')
def display():
    old_fen = request.args.get('board')
    move = request.args.get('move')
    kp = Kidpawn(old_fen)

    if move:
        try:
            success, msg = kp.move(move)
        except Exception as e:
            msg = str(e)
    else:
        msg = "your turn"
    board_svg = kp.svg()
    board_fen = kp.fen()
    return f"""
        <html>
            <h1>Kidpawn</h1>
            {board_svg}
            <br/>
            <h3>{msg}</h3>
            <form>
                Enter your move: <input name="move" />
                <input type="hidden" name="board" value="{board_fen}" />
                <input type="submit" value="Move" />
            </form>
        </html>
    """

if __name__=='__main__':
    app.run()
