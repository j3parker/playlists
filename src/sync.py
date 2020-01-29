import os
import pathlib
import yaml

def process_yaml_file(f):
    doc = yaml.load(f, Loader=yaml.SafeLoader)
    print(doc)

for path in pathlib.Path('.').glob('*.yaml'):
    with open(path) as f:
        process_yaml_file(f)
