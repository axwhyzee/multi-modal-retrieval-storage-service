from flask import Flask, Response, request
from flask_cors import CORS

from adapters.event_publisher import AbstractPublisher, RedisPublisher
from adapters.repository import AbstractRepository, S3Repository
from service_layer.services import add_doc, get_doc

app = Flask(__name__)
CORS(app)

repo: AbstractRepository = S3Repository()
publisher: AbstractPublisher = RedisPublisher()


@app.route("/add", methods=["POST"])
def add():
    if "file" not in request.files:
        return "No file attached", 400
    if "doc_id" not in request.form:
        return "No document ID provided", 400
    try:
        add_doc(
            doc_id=request.form["doc_id"],
            doc_bytes=request.files["file"].read(),
            repo=repo,
            publisher=publisher,
        )
    except Exception as e:
        return str(e), 400
    return "Done", 200


@app.route("/get/<path:doc_id>", methods=["GET"])
def get(doc_id: str):
    doc_bytes = get_doc(doc_id=doc_id, repo=repo)
    return Response(doc_bytes)


if __name__ == "__main__":
    app.run(port=5000)
