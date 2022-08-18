import yaml

with open('emails_to_send.yml') as fh:
    read_data = yaml.load(fh, Loader=yaml.FullLoader)

# Print YAML data before sorting
print(read_data)