from flask import Flask, request, Response
from flask_cors import CORS

from repository import AbstractRepository, S3Repository
from config import bootstrap


repo: AbstractRepository

app = Flask(__name__)
CORS(app)


@app.route("/store", methods=["POST"])
def store():
    if "file" not in request.files:
        return "No file attached", 400
    if "doc_id" not in request.form:
        return "No document ID provided", 400

    doc_id = request.form["doc_id"]
    doc_bytes = request.files['file'].read()    
    repo.add(doc_id, doc_bytes)
    return "Done", 500


@app.route("/get/<path:doc_id>", methods=["GET"])
def get(doc_id: str):
    doc_bytes = repo.get(doc_id)
    return Response(doc_bytes, content_type="binary/octet-stream")


if __name__ == "__main__":
    bootstrap()
    repo = S3Repository()
    app.run(port=5000)
