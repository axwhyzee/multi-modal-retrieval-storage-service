from flask import Flask, Response, request
from flask_cors import CORS

from repository import S3Repository

app = Flask(__name__)
CORS(app)

repo = S3Repository()


@app.route("/add", methods=["POST"])
def add():
    if "file" not in request.files:
        return "No file attached", 400
    if "key" not in request.form:
        return "No object ID provided", 400
    try:
        data = request.files["file"].read()
        key = request.form["key"]
        repo.add(data, key)
    except Exception as e:
        return str(e), 400
    return "Done", 200


@app.route("/get/<path:key>", methods=["GET"])
def get(key: str):
    data = repo.get(key)
    return Response(data)


if __name__ == "__main__":
    app.run(port=5000)
