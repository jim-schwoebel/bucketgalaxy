import os, click, rich, json, datetime, time
import boto3
from azure.storage.blob import BlobServiceClient
from google.cloud import storage
from dotenv import load_dotenv

from helpers import welcome, get_settings, cli_commands

try:
    # load settings if they exist, assuming they work.
    settings = json.load(open('settings.json'))
except:
    # reload settings
    get_settings.reload()
    settings = json.load(open('settings.json'))

@click.command()
@click.option("--command", help="Command to operate on a bucket (see readme.md - e.g. ['upload_object','delete_object','list_objects','download_objects','delete_bucket'])")
    
def api_init(command):
    # actual api response/description routes
    if command == 'init':
        get_settings.reload()
    else:
        cli_commands.get_response(command, settings)

if __name__ == '__main__':
    api_init()