import boto3
from botocore.exceptions import ClientError

ENDPOINT_URL = "http://localhost:8000"
REGION_NAME = "ap-northeast-1"
TABLE_NAME = "sample_items"


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

    print("delete table")
    table.delete()
    table.wait_until_not_exists()


def make_table(dynamodb):
    print("create table")
    table = dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"},
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5,
        },
    )
    table.wait_until_exists()
    return table


def set_data(table):
    print("set data")
    items = [
        {"id": "item-001", "name": "banana", "quantity": 150},
        {"id": "item-002", "name": "orange", "quantity": 154},
        {"id": "item-003", "name": "apple", "quantity": 100},
    ]

    for item in items:
        table.put_item(Item=item)


def get_data(table):
    print("get data")
    response = table.scan()
    rows = sorted(response["Items"], key=lambda item: item["id"])
    for row in rows:
        print(
            "Data row = (%s, %s, %s)"
            % (str(row["id"]), str(row["name"]), str(row["quantity"]))
        )


def main():
    dynamodb = connect_dynamodb()
    delete_table_if_exists(dynamodb)
    table = make_table(dynamodb)
    set_data(table)
    get_data(table)


if __name__ == "__main__":
    main()
