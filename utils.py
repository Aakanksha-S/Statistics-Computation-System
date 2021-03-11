from datetime import datetime, timedelta

from config import TIME_THRESHOLD_IN_SECONDS


def is_before_cutoff(timestamp):
    """
    checks if transaction is older than threshold (60s)
    """
    cutoff = (
        datetime.utcnow() - timedelta(seconds=TIME_THRESHOLD_IN_SECONDS)
    ).isoformat()
    return timestamp < cutoff


def is_in_future(timestamp):
    """
    checks if transaction timestamp is in future
    """
    return timestamp > datetime.utcnow().isoformat()


def is_eligible(transaction):
    """
    checks if transaction is within the threshold (60s)
    """
    cutoff = str(
        (datetime.utcnow() - timedelta(seconds=TIME_THRESHOLD_IN_SECONDS)).isoformat()
    )
    return transaction["timestamp"] >= cutoff
