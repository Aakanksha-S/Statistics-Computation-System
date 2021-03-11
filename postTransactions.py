from flask import Flask, json, request, url_for,jsonify
from flask_api import FlaskAPI, status, exceptions
from datetime import datetime, timedelta

def postTransactions(amount,timestamp,transactions):
	transactions.append({"amount" : amount,"Timestamp" : timestamp})


def post_transactions_handler(request,transactions):
	if request.method == 'POST':
		try:
			amount = request.data.get('amount')
			timestamp = request.data.get('timestamp')
		except:
			return "", status.HTTP_400_BAD_REQUEST

		old_timestamp = datetime.now() - timedelta(seconds=60)
		if timestamp < str(old_timestamp): 
			return "", status.HTTP_204_NO_CONTENT	

		postTransactions(amount,timestamp,transactions)
		return "", status.HTTP_201_CREATED

	elif request.method == 'DELETE':
		transactions.clear()
		return "", status.HTTP_204_NO_CONTENT