from flask import Flask
app = Flask("pawnobot")

@app.route('/')
def display():
    return "welcome to pawnobot"

if __name__=='__main__':
    app.run()
