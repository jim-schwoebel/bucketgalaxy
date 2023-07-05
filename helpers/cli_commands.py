import os, json
import boto3
from azure.storage.blob import BlobServiceClient
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

# other
import time, click
from tqdm import tqdm
from rich import print_json
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.columns import Columns
from rich.panel import Panel
from rich.markdown import Markdown

def get_s3_client(cloud_provider: str):
    # aws credentials
    if cloud_provider == 'aws':
        aws_client = boto3.client("s3", 
                                 aws_access_key_id=os.getenv('AWS_ACCESS_KEY'), 
                                 aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        return aws_client
    # azure credentials
    elif cloud_provider == 'azure':
        azure_connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        azure_client = BlobServiceClient.from_connection_string(azure_connect_str)
        return azure_client
    # gcp credentials
    elif cloud_provider == 'gcp':
        gcp_key_path = os.getenv('GCP_KEY')  
        gcp_client = storage.Client.from_service_account_json(gcp_key_path)
        return gcp_client
    else:
        return None

# functions
def upload_cloud_object(cloud_provider: str, object_path: str, bucket_name: str):
    print(f"Uploading objects in {cloud_provider} ({bucket_name}):")
    if cloud_provider == "azure":
        blob_service_client=get_s3_client(cloud_provider)
        container_client = blob_service_client.get_container_client(bucket_name)
        with open(object_path, "rb") as data:
            container_client.upload_blob(name=os.path.basename(object_path), data=data)
    elif cloud_provider == "aws":
        s3=get_s3_client(cloud_provider)
        with open(object_path, "rb") as data:
            s3.upload_fileobj(data, bucket_name, os.path.basename(object_path))
    elif cloud_provider == "gcp":
        storage_client=get_s3_client(cloud_provider)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(os.path.basename(object_path))
        with open(object_path, "rb") as data:
            blob.upload_from_file(data)
    else:
        print(f"Invalid cloud provider specified. {cloud_provider}")

def delete_cloud_object(cloud_provider: str, object_name: str, bucket_name: str):
    print(f"Deleting objects in {cloud_provider} ({bucket_name}):")
    if cloud_provider == "azure":
        blob_service_client=get_s3_client(cloud_provider)
        container_client = blob_service_client.get_container_client(bucket_name)
        container_client.delete_blob(object_name)
    elif cloud_provider=="aws":
        s3=get_s3_client(cloud_provider)
        s3.delete_object(Bucket=bucket_name, Key=object_name)
    elif cloud_provider == "gcp":
        storage_client=get_s3_client(cloud_provider)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(object_name)
        blob.delete()
    else:
        print(f"Invalid cloud provider specified. {cloud_provider}")

def list_objects_by_bucket(cloud_provider: str, bucket_name: str):
    print(f"Objects in {cloud_provider} ({bucket_name}):")
    if cloud_provider == "azure":
        blob_service_client=get_s3_client(cloud_provider)
        container_client = blob_service_client.get_container_client(bucket_name)
        blobs = container_client.list_blobs()
        for blob in blobs:
            print(blob.name)
    elif cloud_provider == "aws":
        s3=get_s3_client(cloud_provider)
        objects = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in objects:
            for obj in objects['Contents']:
                print(obj['Key'])
    elif cloud_provider == "gcp":
        storage_client=get_s3_client(cloud_provider)
        bucket = storage_client.get_bucket(bucket_name)
        blobs = storage_client.list_blobs(bucket)
        for blob in blobs:
            print(blob.name)
    else:
        print(f"Invalid cloud provider: {cloud_provider}")

def download_objects_by_bucket(cloud_provider: str, bucket_name: str, destination_folder: str):
    print(f"Downloading objects from {cloud_provider} ({bucket_name})")
    if cloud_provider == "azure":
        blob_service_client=get_s3_client(cloud_provider)
        container_client = blob_service_client.get_container_client(bucket_name)
        blobs = container_client.list_blobs()
        for blob in blobs:
            blob_client = container_client.get_blob_client(blob.name)
            destination_path = os.path.join(destination_folder, blob.name)
            with open(destination_path, "wb") as file:
                file.write(blob_client.download_blob().readall())
    elif cloud_provider == "aws":
        s3=get_s3_client(cloud_provider)
        objects = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in objects:
            for obj in objects['Contents']:
                key = obj['Key']
                destination_path = os.path.join(destination_folder, key)
                s3.download_file(bucket_name, key, destination_path)
    elif cloud_provider == "gcp":
        storage_client=get_s3_client(cloud_provider)
        bucket = storage_client.get_bucket(bucket_name)
        blobs = storage_client.list_blobs(bucket)
        for blob in blobs:
            destination_path = os.path.join(destination_folder, blob.name)
            blob.download_to_filename(destination_path)
    else:
        print(f"Invalid cloud provider: {cloud_provider}")

# create bucket 
def create_bucket(cloud_provider: str, bucket_name: str):
    if cloud_provider == "azure":
        blob_service_client=get_s3_client(cloud_provider)
        container_name = bucket_name
        container_client = blob_service_client.create_container(container_name)
    elif cloud_provider == "aws":
        s3 = get_s3_client(cloud_provider)
        response = s3.create_bucket(Bucket=bucket_name)
    elif cloud_provider == "gcp":
        storage_client = get_s3_client(cloud_provider)
        bucket = storage_client.create_bucket(bucket_name)
    else:
        print(f"Invalid cloud provider: {cloud_provider}")

def delete_bucket(cloud_provider: str, bucket_name: str):
    print(f"Deleting bucket {bucket_name} from {cloud_provider}")
    if cloud_provider == "azure":
        blob_service_client=get_s3_client(cloud_provider)
        blob_service_client.delete_container(bucket_name)
    elif cloud_provider == "aws":
        s3 = boto3.resource('s3',aws_access_key_id=os.getenv('AWS_ACCESS_KEY'), 
                                 aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        bucket = s3.Bucket(bucket_name)
        bucket.objects.all().delete()
    elif cloud_provider == "gcp":
        storage_client=get_s3_client(cloud_provider)
        bucket = storage_client.get_bucket(bucket_name)
        bucket.delete(force=True)
    else:
        print(f"Invalid cloud provider: {cloud_provider}")
    
def api_loading_screen(message_1: str="Getting response", message_2: str= "Received response", spinner_1: str="bouncingBall", spinner_2: str="moon", immediate_response: bool=False):
    '''
        This function creates a nice waiting screen with Rich text editor for api responses.

        Note can addapt the spinner_1 and spinner_2 arguments with the rich documentation 
        (see python3 -m rich.spinner).

        If you want to skip the loading screen completely, just call this function with immediate_response == True

        https://rich.readthedocs.io/en/stable/reference/status.html
        https://www.brianlinkletter.com/2021/03/using-python-rich-library-status-module/
    '''
    if immediate_response == False:
        console = Console()
        with console.status("[bold white] %s..."%(message_1), spinner=spinner_1) as status:
            time.sleep(2)
            status.update("[bold blue] %s, rendering..."%(message_2), spinner=spinner_2)
            time.sleep(1)
    else: 
        pass 

## API commands - https://docs.digitalocean.com/reference/api/api-reference/
def get_response(command: str, settings: dict):
    if command == 'upload_object':
        object_path = click.prompt(click.style('what is the local object path? (e.g. jim.wav)\n', fg='cyan'), type=str)
        upload_cloud_object(cloud_provider=settings['cloud_provider'], object_path=object_path, bucket_name=settings['bucket_name'])
    elif command == 'delete_object':
        object_name = click.prompt(click.style('what is the object name in the bucket to delete? (e.g. jim.wav)\n', fg='cyan'), type=str)
        delete_cloud_object(cloud_provider=settings['cloud_provider'], object_name=object_name, bucket_name=settings['bucket_name'])
    elif command == 'list_objects':
        list_objects_by_bucket(cloud_provider=settings['cloud_provider'], bucket_name=settings['bucket_name'])
    elif command == 'download_objects':
        download_objects_by_bucket(cloud_provider=settings['cloud_provider'], bucket_name=settings['bucket_name'], destination_folder=settings['destination_folder'])
    elif command == 'create_bucket':
        bucket_name = click.prompt(click.style('what is the name of the bucket you want to create? (e.g. test-aaskflasf - blank for random uuid)\n', fg='cyan'), type=str)
        create_bucket(cloud_provider=settings['cloud_provider'], bucket_name=bucket_name)
        settings=json.load(open('settings.json'))
        settings['bucket_name'] = bucket_name
        jsonfile=open('settings.json','w')
        json.dump(settings, jsonfile)
        jsonfile.close()
    elif command == 'delete_bucket':
        delete_bucket(cloud_provider=settings['cloud_provider'], bucket_name=settings['bucket_name'])
    else: 
        api_loading_screen()
        console = Console()
        table = Table(show_header=True, header_style="bold white")
        columns=['command', 'description']
        for column in columns:
            table.add_column(column.title(), style="dim", justify="left")

        table.add_row('upload_object', 'upload an object to a bucket')
        table.add_row('delete_object', 'delete an object in a bucket')
        table.add_row('list_objects', 'list objects in a bucket')
        table.add_row('download_objects', 'download all objects to a local destination folder')
        table.add_row('create_bucket', 'create a new bucket (and change default settings.json file there)')   
        table.add_row('delete_bucket', 'delete all objects in the defined bucket (and the bucket itself)')
        console.print(table)




