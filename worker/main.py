import requests
import os
import logging
import time

def healthcheck():
    try:
        url = f"http://qdrant_database:6333/healthz"
        res = requests.get(url)
        if res.status_code == 200:
            return res.text
    except Exception as e:
        logging.info(e)
        return "not healthy"

def download_file(url, local_filename):
    # Check if file already exists
    if not os.path.exists(local_filename):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded {local_filename}")
    else:
        print(f"{local_filename} already exists. Skipping download.")

    return local_filename

def recover_from_snapshot_with_file(collection_name, file_path, wait=True, priority=None):
    url = f"http://qdrant_database:6333/collections/{collection_name}/snapshots/upload"

    params = {
        "wait": str(wait).lower(),
    }

    if priority is not None:
        params['priority'] = priority

    with open(file_path, 'rb') as file:
        files = {'snapshot': file}
        response = requests.post(url, files=files, params=params)

    # Check response status and content
    print(f"Status Code for {collection_name}:", response.status_code)
    print(f"Response Content for {collection_name}:", response.text)

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": "Response not in JSON format", "status_code": response.status_code, "response": response.text}

def construct_snapshot_url(collection_name):
    # Assuming a consistent URL pattern for all collections
    return f"https://eu-west-hasura.s3.eu-west-3.amazonaws.com/{collection_name}.snapshot"


print("IN MAIN")
if __name__ == "__main__":
    while healthcheck() != "healthz check passed":
        logging.info("Qdrant not healthy... sleeping")
        time.sleep(1)

    # List of collections to process
    collections = ["Album", "article", "boolean", "image_recipe", "multimodal_recipe", "text_recipe"]

    # Download and recover snapshots for each collection
    for collection_name in collections:
        url = construct_snapshot_url(collection_name)
        local_filename = f"/app/snapshots/{collection_name}.snapshot"
        download_file(url, local_filename)
        response = recover_from_snapshot_with_file(collection_name, local_filename)
        print(response)