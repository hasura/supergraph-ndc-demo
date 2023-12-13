import os
import yaml
import json

SUBGRAPH_DOCKERS = {
    "turso": "http://turso:8101",
    "qdrant": "http://qdrant:8102",
    "functions": "http://functions:8080"
}

EXCLUDED_SUBGRAPHS = []

class CustomLoader(yaml.SafeLoader):
    """
    Custom YAML loader that treats '=' as a string.
    """

    def __init__(self, *args, **kwargs):
        super(CustomLoader, self).__init__(*args, **kwargs)

        # Add constructor for handling '='
        self.add_constructor(u'tag:yaml.org,2002:value', type(self).construct_yaml_str)

    def construct_yaml_str(self, node):
        return self.construct_scalar(node)

yaml.SafeLoader = CustomLoader

def load_yaml_files(directory):
    subgraph_data = {}

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.haml') or file.endswith('.hml'):
                path = os.path.join(root, file)
                subgraph = None
                if path.startswith("ddn-metadata/subgraphs/"):
                    subgraph = path.replace("ddn-metadata/subgraphs/", "").split("/")[0]
                    if subgraph_data.get(subgraph, None) is None:
                        subgraph_data[subgraph] = []
                    with open(path, 'r') as stream:
                        try:
                            yaml_content = list(yaml.safe_load_all(stream))
                            yaml_items = []
                            for item in yaml_content:
                                if item["kind"] == "DataConnector":
                                    if subgraph in SUBGRAPH_DOCKERS:
                                        item["definition"]["url"]["singleUrl"] = SUBGRAPH_DOCKERS[subgraph]
                                yaml_items.append(item)
                            if subgraph not in EXCLUDED_SUBGRAPHS:
                                subgraph_data[subgraph].extend(yaml_items)
                        except yaml.YAMLError as exc:
                            print(f"Error loading YAML from {path}: {exc}")

    return subgraph_data

# Replace 'ddn-metadata' with the path to the directory you want to search
directory_path = 'ddn-metadata'
subgraph_data = load_yaml_files(directory_path)

subgraphs = []
for subgraph_name, subgraph_items in subgraph_data.items():
    subgraphs.append({
        "name": subgraph_name,
        "objects": subgraph_items
    })

subgraph_data = {
    "version": "v2",
    "subgraphs": subgraphs
}

# Dump to JSON file
with open('engine/metadata.json', 'w') as json_file:
    json.dump(subgraph_data, json_file, indent=4)
