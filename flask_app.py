import flask

app = flask.Flask(__name__)


@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/spx')
def spx():
    return "Level of the SPX S&P 500 index"

if __name__ == "__main__":
    app.run()