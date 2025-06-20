from flask import Flask

app = Flask(__name__)

@app.route('/')
def user():
    return 'Hello world'

(__name__) == ('__main__')
app.run(debug=True)
