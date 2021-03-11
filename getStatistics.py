from flask import Flask, json, request, url_for,jsonify
from flask_api import FlaskAPI, status, exceptions
from datetime import datetime, timedelta
from decimal import Decimal
 

def getStatistics(transactions):
	start_timestamp = datetime.now() - timedelta(seconds=60)
	amount_list = []
	for obj in transactions:
		if obj["Timestamp"] >= str(start_timestamp):
			amount_list.append(Decimal(obj["amount"]))
	print(amount_list)
	sum_of_amounts = sum(amount_list)
	count_of_amounts = len(amount_list)
	avg_of_amounts = sum_of_amounts / count_of_amounts
	max_of_amounts = max(amount_list)
	min_of_amounts = min(amount_list)
	return {"sum" : sum_of_amounts.to_eng_string(),"avg" : avg_of_amounts.to_eng_string(), "max" : max_of_amounts.to_eng_string(), "min" : min_of_amounts.to_eng_string(), "count" : count_of_amounts},

	

def get_statistics_handler(request,transactions):
	return getStatistics(transactions)