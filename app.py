import concurrent.futures

from flask import request
from flask_api import FlaskAPI

from get_statistics import get_statistics
from transactions import execute_transaction

app = FlaskAPI(__name__)

transactions_store = []


@app.route("/statistics", methods=["GET"])
def get_statistics_handler():
    """
    Method: GET
    Payload : No Payload
    Response : Statistics of transactions with timestamp within the threshold (60s)
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(get_statistics, transactions_store)
        return future.result()


@app.route("/transactions", methods=["POST", "DELETE"])
def transactions_handler():
    """
    Method: POST/DELETE
    Payload : json obj containing Amount, Timestamp
    Response : Empty body
    """
    method = request.method
    request_body = request.data
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(
            execute_transaction, transactions_store, method, request_body
        )
        return future.result()


if __name__ == "__main__":
    app.run(threaded=True)
