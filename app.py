import logging

from event_core.adapters.services.exceptions import FailedToStore
from flask import Flask, request
from flask_cors import CORS

from bootstrap import bootstrap
from handlers import (
    handle_add,
    handle_delete,
    handle_get,
    handle_len,
    handle_list,
)


def create_app():
    logging.basicConfig(level=logging.INFO)
    app = Flask(__name__)
    CORS(app)
    bootstrap()
    return app


app = create_app()


@app.route("/add", methods=["POST"])
def add():
    REQUIRED_FIELDS = (
        "key",
        "type",
    )
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
    repo_obj_type = request.form["type"]

    try:
        handle_add(data, key, repo_obj_type)
    except FailedToStore as e:
        return str(e), 400
    except KeyError as e:
        return f"Unsupported RepoObject type {repo_obj_type}"
    return "Success", 200


@app.route("/get/<path:key>", methods=["GET"])
def get(key: str):
    return handle_get(key), 200


@app.route("/delete/<path:key>", methods=["GET"])
def delete(key: str):
    handle_delete(key)
    return "Success", 200


@app.route("/len", methods=["GET"])
def length():
    return str(handle_len()), 200


@app.route("/list", methods=["GET"])
def list_keys():
    return handle_list(), 200


if __name__ == "__main__":
    app.run(port=5001)
