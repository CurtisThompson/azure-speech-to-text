import yaml

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

print(config['azure']['key'])
print(config['azure']['endpoint'])
print(config['azure']['wait_ms'])
print(config['data']['input_path'])
print(config['data']['output_path'])
print(config['verbose'])