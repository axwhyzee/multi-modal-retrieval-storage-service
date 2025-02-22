from event_core.adapters.exceptions import FailedToStore
from flask import Flask, Response, request
from flask_cors import CORS

from services.handlers import handle_add, handle_delete, handle_get

app = Flask(__name__)
CORS(app)


@app.route("/add", methods=["POST"])
def add():
    if "file" not in request.files:
        return "File required", 400
    if "key" not in request.form:
        return "`key` provided", 400
    if "obj_type" not in request.form:
        return "`obj_type` required"

    data = request.files["file"].read()
    key = request.form["key"]
    obj_type = request.form["obj_type"]

    try:
        handle_add(data, key, obj_type)
    except FailedToStore as e:
        return str(e), 400
    except KeyError as e:
        return f"Unsupported object type {obj_type}"
    return "Success", 200


@app.route("/get/<path:key>", methods=["GET"])
def get(key: str):
    return Response(handle_get(key))


@app.route("/delete/<path:key>", methods=["GET"])
def delete(key: str):
    handle_delete(key)
    return "Success", 200


if __name__ == "__main__":
    app.run(port=5001)
