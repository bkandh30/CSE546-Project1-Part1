import boto3
import csv

sdb_client = boto3.client('sdb', region_name='us-east-1') 

DOMAIN_NAME = "1229592821-simpleDB"

sdb_client.create_domain(DomainName=DOMAIN_NAME)

print("Domain created successfully.")

def insert_into_simpledb(file_path):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            item_name = row['Image']  
            attributes = [
                {'Name': 'Results', 'Value': row['Results'], 'Replace': True}
            ]
            sdb_client.put_attributes(
                DomainName=DOMAIN_NAME,
                ItemName=item_name,
                Attributes=attributes
            )
    print("Data inserted successfully.")

file_path = '/Users/bhavyakandhari/Downloads/Classification Results on Face Dataset (1000 images).csv'
insert_into_simpledb(file_path)
