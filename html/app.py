from flask import Flask, request


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def hello_world(path=None):
    print(path)
    print(request.method)
    print(request.form)
    return f'Hello, World! {path}'

app.run(debug=True, port=8000, host='0.0.0.0')
