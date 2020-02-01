from flask import Flask
app = Flask("kidpawn")

from kidpawn import Kidpawn

@app.route('/')
def display():
    kp = Kidpawn()
    return kp.svg()

if __name__=='__main__':
    app.run()
