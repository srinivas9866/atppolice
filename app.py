from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, List

from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
RESPONSES_PATH = os.path.join(BASE_DIR, "responses.json")

app = Flask(__name__, static_folder=BASE_DIR, static_url_path="/static")


def load_responses() -> List[Dict[str, Any]]:
    if not os.path.exists(RESPONSES_PATH):
        return []
    try:
        with open(RESPONSES_PATH, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def save_responses(data: List[Dict[str, Any]]) -> None:
    with open(RESPONSES_PATH, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


@app.route("/")
def safety_form() -> Any:
    return send_from_directory(BASE_DIR, "safety-form.html")


@app.route("/admin")
def admin_panel() -> Any:
    return send_from_directory(BASE_DIR, "admin-analytics.html")



@app.route("/submit", methods=["POST"])
def submit_response() -> Any:
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"ok": False, "error": "Invalid payload"}), 400

    payload["submittedAt"] = datetime.now().isoformat(timespec="seconds")
    payload["id"] = int(datetime.now().timestamp() * 1000)

    responses = load_responses()
    responses.append(payload)
    save_responses(responses)

    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
