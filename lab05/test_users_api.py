import json
from datetime import datetime
from pathlib import Path

import pytest
import requests

pytestmark = pytest.mark.api
BASE_URL = "https://jsonplaceholder.typicode.com"
RESULTS = Path(__file__).parent / "results"


def request(method, path, body=None):
    response = requests.request(method, BASE_URL + path, json=body, timeout=30)
    RESULTS.mkdir(exist_ok=True)
    evidence = {"executed_at": datetime.now().astimezone().isoformat(), "method":method,"url":response.url,"request_body":body,"status_code":response.status_code,"content_type":response.headers.get("Content-Type"),"elapsed_ms":round(response.elapsed.total_seconds()*1000,2),"response_body":response.json()}
    filename = method.lower() + "_" + path.strip('/').replace('/', '_') + ".json"
    (RESULTS / filename).write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    return response


def test_get_user():
    response = request("GET", "/users/1")
    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]
    body = response.json()
    assert isinstance(body, dict)
    assert {"id", "name", "username", "email", "address", "company"} <= body.keys()
    assert body["id"] == 1
    assert body["username"] == "Bret"
    assert all(isinstance(body[key], str) for key in ("name", "username", "email"))
    assert isinstance(body["address"], dict)


def test_create_user():
    data = {"name":"Student Test", "username":"student_test", "email":"student@example.com"}
    response = request("POST", "/users", data)
    assert response.status_code == 201
    assert "application/json" in response.headers["Content-Type"]
    body = response.json()
    assert isinstance(body, dict) and isinstance(body.get("id"), int)
    assert body["id"] == 11
    assert {key: body[key] for key in data} == data


def test_update_user():
    data = {"id":1, "name":"Updated Student", "username":"student_updated", "email":"updated@example.com"}
    response = request("PUT", "/users/1", data)
    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]
    body = response.json()
    assert isinstance(body, dict) and isinstance(body.get("id"), int)
    assert body == data


def test_missing_user():
    response = request("GET", "/users/99999")
    assert response.status_code == 404
    assert response.json() == {}
