### Qdrant Setup Worker

This script is designed to run once Qdrant is started. It will download collection snapshots from an S3 bucket and upload them into the locally running Qdrant instance.

This is a bit of a quick and dirty script. 

You can edit the constants at the top of the script if you have an S3 bucket with your own Qdrant collection snapshots in it.

This doesn't use boto3, as the snapshots are set to public.

```python
# Change these to point to your own S3 bucket containing snapshots.
# This points to a public S3 bucket that contains uploads of Qdrant Snapshots that can be generated in the Qdrant Dashboard.
URL_PATTERN = "https://eu-west-hasura.s3.eu-west-3.amazonaws.com/{collection_name}.snapshot"
# List of collections to process
COLLECTIONS = ["Album", "article", "boolean", "image_recipe", "multimodal_recipe", "text_recipe"]
```

You can create an S3 bucket, and place snapshots in them, this will upload them on startup.

It ONLY downloads the snapshots if they are not already on disk as it makes use of a Docker volume.

It will UPLOAD the snapshots each time you start the container, resetting things to the default state.


In the Docker Compose File this is the snapshot-uploader service:

```
  snapshot-uploader:
    build:
      context: ./worker
      dockerfile: Dockerfile
    volumes:
      - snapshot-data:/app/snapshots
    depends_on:
      - qdrant_database
```