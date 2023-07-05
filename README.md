# bucketgalaxy
a repo for cloud-agnostic s3 bucket manipulations (gcp, aws, and azure).

## getting started

Install dependencies
```
virtualenv env 
source env/bin/activate
pip3 install -r requirements.txt
```
Recommend adding a .env
```
nano .env
```
with these env vars
```
# AWS environment vars
AWS_ACCESS_KEY=string
AWS_SECRET_ACCESS_KEY=string

# Azure environment vars
AZURE_KEY=string
AZURE_STORAGE_CONNECTION_STRING=string

# GCP environment vars
GCP_KEY=file.json
```
Now set up the environment (AWS, GCP, or Azure)
```
python3 cli.py
```

## available operations
These are the available operations:

```
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Command          ┃ Description                                               ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ upload_object    │ upload an object to a bucket                              │
│ delete_object    │ delete an object in a bucket                              │
│ list_objects     │ list objects in a bucket                                  │
│ download_objects │ download all objects to a local destination folder        │
│ create_bucket    │ create a new bucket (and change default settings.json     │
│                  │ file there)                                               │
│ delete_bucket    │ delete all objects in the defined bucket (and the bucket  │
│                  │ itself)                                                   │
└──────────────────┴───────────────────────────────────────────────────────────┘
```

More to come later.