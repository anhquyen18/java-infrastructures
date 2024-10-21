import yaml

def read_yml_file(file_path, environment):
    with open(file_path, 'r') as file:
        params = yaml.safe_load(file)
        return params.get(environment)