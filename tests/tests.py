from datetime import datetime, timedelta

import pytest
import requests


def test_get_transaction():
    response = requests.get("http://localhost:5000/statistics")
    assert response.status_code == 200


def test_post_transaction_within_60seconds():
    timestamp = datetime.utcnow() - timedelta(seconds=20)
    payload = {"amount": "1.1", "timestamp": timestamp.isoformat()}
    response = requests.post("http://localhost:5000/transactions", data=payload)
    assert response.text == "" and response.status_code == 201


def test_delete_transactions():
    response = requests.delete("http://localhost:5000/transactions")
    assert response.text == "" and response.status_code == 204


def test_post_transaction_older_than_60seconds():
    timestamp = datetime.utcnow() - timedelta(minutes=1)
    payload = {"amount": "1.1", "timestamp": timestamp.isoformat()}
    response = requests.post("http://localhost:5000/transactions", data=payload)
    assert response.text == "" and response.status_code == 204


def test_post_transaction_future():
    timestamp = datetime.utcnow() + timedelta(seconds=60)
    payload = {"amount": "1.1", "timestamp": timestamp.isoformat()}
    response = requests.post("http://localhost:5000/transactions", data=payload)
    assert response.text == "" and response.status_code == 422


def test_unparsable_json_invalid_timestamp():
    payload = {"amount": "1.1", "timestamp": "1.1"}
    response = requests.post("http://localhost:5000/transactions", data=payload)
    assert response.text == "" and response.status_code == 422


def test_unparsable_json_invalid_amount():
    payload = {"amount": True, "timestamp": "1.1"}
    response = requests.post("http://localhost:5000/transactions", data=payload)
    assert response.text == "" and response.status_code == 422


def test_invalid_json():
    with pytest.raises(ValueError):
        timestamp = datetime.utcnow() - timedelta(seconds=40)
        payload = ["amount", "1.1", "timestamp", timestamp]
        requests.post("http://localhost:5000/transactions", data=payload)


def test_get_statistics_successfully():
    timestamp1 = datetime.utcnow() - timedelta(seconds=40)
    timestamp2 = datetime.utcnow() - timedelta(seconds=50)
    timestamp3 = datetime.utcnow() - timedelta(seconds=30)
    payload1 = {"amount": "1.234", "timestamp": timestamp1.isoformat()}
    payload2 = {"amount": "9.109", "timestamp": timestamp2.isoformat()}
    payload3 = {"amount": "8.786", "timestamp": timestamp3.isoformat()}
    requests.post("http://localhost:5000/transactions", data=payload1)
    requests.post("http://localhost:5000/transactions", data=payload2)
    requests.post("http://localhost:5000/transactions", data=payload3)
    response = requests.get("http://localhost:5000/statistics")

    response_data = {
        "sum": "19.13",
        "avg": "6.38",
        "max": "9.11",
        "min": "1.23",
        "count": 3,
    }
    return eval(response.text) == response_data


def test_get_statistics_with_no_transactions():
    timestamp1 = datetime.utcnow() - timedelta(minutes=1)
    timestamp2 = datetime.utcnow() - timedelta(minutes=2)
    timestamp3 = datetime.utcnow() - timedelta(minutes=3)
    payload1 = {"amount": "1.234", "timestamp": timestamp1.isoformat()}
    payload2 = {"amount": "9.109", "timestamp": timestamp2.isoformat()}
    payload3 = {"amount": "8.786", "timestamp": timestamp3.isoformat()}
    requests.post("http://localhost:5000/transactions", data=payload1)
    requests.post("http://localhost:5000/transactions", data=payload2)
    requests.post("http://localhost:5000/transactions", data=payload3)

    response = requests.get("http://localhost:5000/statistics")
    response_data = {}
    return eval(response.text) == response_data
