import os
import pathlib
import yaml

def process_yaml_file(doc):
    print(doc)

def main():
    for path in pathlib.Path('.').glob('*.yaml'):
        with open(path) as f:
            doc = yaml.load(f, Loader=yaml.SafeLoader)
            process_yaml_file(doc)

if __name__ == "__main__":
    main()
