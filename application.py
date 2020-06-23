#!flask/bin/python
import json, random, string
from flask import Flask, Response, render_template, request, redirect, send_from_directory
import boto3
from botocore.exceptions import ClientError
import os
import dynamodb
import random
from datetime import datetime, timezone
#from helloworld.flaskrun import flaskrun

application = Flask(__name__)

@application.route('/', methods=['GET'])
def url():
    return render_template("home.html")

@application.route('/createvm', methods=['POST'])
def createvm():
    if request.method == 'POST':
        request.form.get
        ami = request.form.get('ami')
        print("image - ", ami)
        instancetype = request.form.get('instancetype')
        print("instancetype - ", instancetype)
        orderid = processvmrequest(ami, instancetype)
        return render_template("home.html", orderid=orderid)

def processvmrequest(imageid, instancetype):
    # Get the service resource
    sqs = boto3.resource('sqs')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='vra_createvm')

    orderid = str(random.randrange(0,100000,4))
    #imageid = 'ami-09d95fab7fff3776c'
    #instancetype = 't2.micro'

    data = '{"orderid": "' + orderid + '", "imageid":"' + imageid + '", "instancetype": "' + instancetype + '"}'

    # send message to queue..
    print ('Sending message to queue, message - ', data)
    response = queue.send_message(
        MessageBody=data
    )

    # The response is NOT a resource, but gives you a message ID and MD5
    print ('message id...')
    print(response.get('MessageId'))
    print(response.get('MD5OfMessageBody'))

    # add order details to db
    print ('order details added to table...')
    dynamodb.add_order(orderid, datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S"), imageid, instancetype, 'submitted', '')

    return orderid

if __name__ == '__main__':
    application.run(
        debug="true",
        host="0.0.0.0",
        port=5000
    )