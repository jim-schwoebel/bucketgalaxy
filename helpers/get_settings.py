import os, click, rich, json, datetime, time
from rich.console import Console
from rich.table import Table

def reload():
    # setup the CLI properly using an existing digitalocean API token.
    valid_key = False

    credentials=dict()
    settings=dict()

    while valid_key == False:
        cloud_provider = click.prompt(click.style('what cloud provider are you connecting to? ["aws","azure","gcp"]\n', fg='cyan'), type=str)
        bucket_name = click.prompt(click.style('what is your bucket name? (e.g. "test-bucket")\n', fg='cyan'), type=str)
        destination_folder = click.prompt(click.style('what is your destination folder for downloads? (e.g. "download/")\n', fg='cyan'), type=str)
        
        if cloud_provider in ["aws","azure","gcp","digitalocean"]:
            if cloud_provider == 'aws':
                aws_access_key = click.prompt(click.style('what is your AWS_ACCESS_KEY_ID\n', fg='cyan'), type=str,  hide_input=True)
                aws_secret_key = click.prompt(click.style('what is your AWS_SECRET_ACCESS_KEY\n', fg='cyan'), type=str,  hide_input=True)
                credentials['aws_access_key'] = aws_access_key
                credentials['aws_secret_key'] = aws_secret_key

            elif cloud_provider == 'azure':
                azure_connection_string = click.prompt(click.style('what is your azure connection string?\n', fg='cyan'), type=str,  hide_input=True)
                credentials['azure_connection_string'] = azure_connection_string

            elif cloud_provider == 'gcp':
                gcp_key_path = click.prompt(click.style('what is your GCP_KEY_PATH? (e.g. "asklf.json")\n', fg='cyan'), type=str,  hide_input=True)
                credentials['gcp_key_path'] = gcp_key_path
        
        settings['cloud_provider']=cloud_provider
        settings['bucket_name']=bucket_name
        settings['destination_folder']=destination_folder
        settings['credentials']=credentials

        # only take the listed database 
        jsonfile=open('settings.json','w')
        json.dump(settings,jsonfile)
        jsonfile.close()
        valid_key = True 

    click.echo(click.style('\n\n✅ Congrats! You are ready to go. \n', bold=True, fg='white'))

