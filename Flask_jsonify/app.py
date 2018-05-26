from flask import Flask, render_template
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def index():
        return render_template("index.html")

@app.route('/sentiment')
def sentiment():
    data = [0.3, 0.5, 0.9]
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == "__main__":
        app.run(host='0.0.0.0', debug=True)

