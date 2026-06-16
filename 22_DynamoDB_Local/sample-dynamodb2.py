import datetime
import random

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

ENDPOINT_URL = "http://localhost:8000"
REGION_NAME = "ap-northeast-1"
TABLE_NAME = "sample_sensors"


def connect_dynamodb():
    return boto3.resource(
        "dynamodb",
        endpoint_url=ENDPOINT_URL,
        region_name=REGION_NAME,
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
    )


def delete_table_if_exists(dynamodb):
    table = dynamodb.Table(TABLE_NAME)
    try:
        table.load()
    except ClientError as err:
        if err.response["Error"]["Code"] == "ResourceNotFoundException":
            return
        raise

    print("--- delete Table ---")
    table.delete()
    table.wait_until_not_exists()


def make_table(dynamodb):
    print("--- make Table ---")
    table = dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {"AttributeName": "device", "KeyType": "HASH"},
            {"AttributeName": "updateday", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "device", "AttributeType": "S"},
            {"AttributeName": "updateday", "AttributeType": "S"},
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5,
        },
    )
    table.wait_until_exists()
    print("table status:", table.table_status)
    return table


def add_table_data(table):
    print("--- add TableData ---")

    temperature = 10
    humidity = 10
    battery = 10
    dt = datetime.datetime.now() + datetime.timedelta(days=-2)

    for _ in range(5):
        for item in ["device1", "device2", "device3"]:
            updateday = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
            table.put_item(
                Item={
                    "device": item,
                    "updateday": updateday,
                    "temperature": temperature,
                    "humidity": humidity,
                    "battery": battery,
                }
            )

            print(
                "device:",
                item,
                "temperature:",
                temperature,
                "humidity:",
                humidity,
                "battery:",
                battery,
                "time:",
                updateday,
            )

            temperature += random.randint(-3, 3)
            humidity += random.randint(-3, 3)
            battery += random.randint(-3, 3)
            dt = dt + datetime.timedelta(milliseconds=5)

        dt = dt + datetime.timedelta(milliseconds=30)


def query_table(table):
    print("--- query Table ---")
    response = table.query(KeyConditionExpression=Key("device").eq("device1"))
    rows = sorted(response["Items"], key=lambda item: item["updateday"])
    for row in rows:
        print(row)


def main():
    dynamodb = connect_dynamodb()
    delete_table_if_exists(dynamodb)
    table = make_table(dynamodb)
    add_table_data(table)
    query_table(table)


if __name__ == "__main__":
    main()
