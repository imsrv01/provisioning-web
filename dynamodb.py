import boto3, time
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('vra_vm_requests')

def add_order(orderid, requested_date, imageid, instancetype, status,vmname):
    response = table.put_item(
        Item = {
            'orderid' : orderid,
            'requested_date': requested_date,
            'imageid' : imageid,
            'instancetype' : instancetype,
            'orderstatus' : status,
            'vmname' : vmname
        }
    )
    return response

def update_order(orderid, status):
    response = table.update_item(
        Key = {
            'orderid' : orderid
        },
        UpdateExpression = "set orderstatus = :s",
        ExpressionAttributeValues = {
            ':s' : status
        }
    )
    return response

if __name__ == '__main__':
    imageid = 'ami-09d95fab7fff3776c'
    instancetype = 't2.micro'
    response = add_order('0006', datetime.now().strftime("%d/%m/%Y %H:%M:%S"), imageid, instancetype, 'in-progress')
    print(response)
    time.sleep(2)
    response = update_order('0006', 'complete')
    print(response)
    