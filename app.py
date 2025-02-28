from event_core.adapters.services.exceptions import FailedToStore
from flask import Flask, request
from flask_cors import CORS

from bootstrap import bootstrap
from handlers import handle_add, handle_delete, handle_get

app = Flask(__name__)
CORS(app)


@app.route("/add", methods=["POST"])
def add():
    REQUIRED_FIELDS = ("key", "obj_type", "modal")
    missing_fields = []
    if "file" not in request.files:
        missing_fields.append("file")
    for field in REQUIRED_FIELDS:
        if field not in request.form:
            missing_fields.append(field)
    if missing_fields:
        return f"({','.join(missing_fields)}) required", 400

    data = request.files["file"].read()
    key = request.form["key"]
    obj_type = request.form["obj_type"]
    modal = request.form["modal"]

    try:
        handle_add(data, key, obj_type, modal)
    except FailedToStore as e:
        return str(e), 400
    except KeyError as e:
        return f"Unsupported object type {obj_type}"
    return "Success", 200


@app.route("/get/<path:key>", methods=["GET"])
def get(key: str):
    return handle_get(key), 200


@app.route("/delete/<path:key>", methods=["GET"])
def delete(key: str):
    handle_delete(key)
    return "Success", 200


if __name__ == "__main__":
    bootstrap()
    app.run(port=5001)
