from flask import Flask
app = Flask("kidpawn")

from kidpawn import Kidpawn

@app.route('/')
def display():
    kp = Kidpawn()
    board_svg = kp.svg()
    board_fen = kp.fen()
    return f"""
        <html>
            <h1>Kidpawn</h1>
            {board_svg}
            <br/>
            <form>
                Enter your move: <input name="move" />
                <input type="hidden" name="board" value="{board_fen}" />
                <input type="submit" value="Move" />
            </form>
        </html>
    """

if __name__=='__main__':
    app.run()
