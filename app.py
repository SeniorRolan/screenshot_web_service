from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return "Привет, мир!"


@app.route('/<name>')
def hello_name(name):
    return f"Привет, {name}!"


if __name__ == '__main__':
    app.run()