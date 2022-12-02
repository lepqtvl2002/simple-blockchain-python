from pymongo import MongoClient
# Creating instance of mongoclient

client = MongoClient("mongodb+srv://admin:thang30102002@cluster0.tqz3n44.mongodb.net/?retryWrites=true&w=majority")
# Create Database
db = client.test


import datetime
import json

import requests
from flask import render_template, redirect, request

from app import app

# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []


def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)


@app.route('/')
def index():
    fetch_posts()
    length = len(posts)

    def filterFnc(x):
        if x["index"] < length - 10:
            return False
        else:
            return True
    selectPosts = filter(filterFnc, posts)
    return render_template(['index.html'],
                           title='STORE MEDICAL HISTORY '
                                 'WITH BLOCKCHAIN',
                           posts=selectPosts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)

@app.route('/book_care_health')
def book_care_health():
  
    return render_template(['book_care_health.html'],
                           title='BOOK CARE HEALTH',
                           patient={},
                           posts={},
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)

@app.route('/search', methods=['POST'])
def search_textarea():
    """
    Search patient
    """
    bhyt = request.form["bhyt"]
    name = request.form["name"]
    birthday = request.form["birthday"]
    phone_number = request.form["phoneNumber"]

    def getPatientById(bhyt):
        for x in db.patients.find():
            if (x["bhyt"] == bhyt):
                return x
        return {}

    patient = getPatientById(int(bhyt))

    if (patient):
        patient["birthday"] = patient["birthday"].strftime('%Y-%m-%d')

        def filterFnc(x):
            if  x["name"] == patient["name"]:
                return True
            else:
                return False

        selectPosts = filter(filterFnc, posts)
        return render_template(['book_care_health.html'],
                           title='BOOK CARE HEALTH',
                           patient=patient,
                           posts=selectPosts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)

    else:
        return render_template(['index.html'],
                           title='NOT FOUND',
                           posts=patient,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)
    


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    name = request.form["name"]
    birthday = request.form["birthday"]
    diagnostic = request.form["diagnostic"]

    post_object = {
        'name': name,
        'birthday': birthday,
        'diagnostic' : diagnostic
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect(CONNECTED_NODE_ADDRESS + '/mine')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M')
