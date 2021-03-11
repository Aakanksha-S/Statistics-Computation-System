import sys
import os

from flask import Flask, json, request, url_for,jsonify
from flask_api import FlaskAPI, status, exceptions

from getStatistics import *
from postTransactions import *
 
api = FlaskAPI(__name__)
 
transactions = []

def parse(jsonStr):
	try:
		json.parse(jsonStr)
	except:
		return "", status.HTTP_422_BAD_REQUEST


@api.route('/statistics', methods=['GET'])
def get_statistics():
	return get_statistics_handler(request,transactions)


@api.route("/transactions",methods=['POST','DELETE'])
def post_transactions():
	return post_transactions_handler(request,transactions)
	
if __name__ == '__main__':
    api.run()