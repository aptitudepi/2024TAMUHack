import boto3

dynamo_client = boto3.client('dynamodb')

def get_club_items():
    return dynamo_client.scan(
        TableName='STEAM-APP-Clubs'
    )
def get_calendar_items():
    return dynamo_client.scan(
        TableName='STEAM-APP-Calendar'
    )