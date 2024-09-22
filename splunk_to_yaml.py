import argparse
import yaml
import re
import os

def infer_type(value):
    """Infer the data type of a configuration value."""
    value = value.strip()
    # Try to interpret as integer
    try:
        return int(value)
    except ValueError:
        pass
    # Try to interpret as float
    try:
        return float(value)
    except ValueError:
        pass
    # Interpret as boolean if applicable
    if value.lower() in ['true', 'false', 'yes', 'no']:
        return value.lower() in ['true', 'yes']
    # Interpret as a list if comma-separated
    if ',' in value:
        return [infer_type(item) for item in value.split(',')]
    # Default to string
    return value

def parse_savedsearches_conf(filename):
    """Parse the savedsearches.conf file into a dictionary."""
    config = {}
    current_section = None
    current_line = ''
    with open(filename, 'r') as file:
        for line in file:
            line = line.rstrip('\n')
            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith('#'):
                continue
            # Handle line continuation with backslash
            if line.strip().endswith('\\'):
                current_line += line.strip()[:-1] + ' '
                continue
            else:
                current_line += line.strip()
            # Process section headers
            if current_line.startswith('[') and current_line.endswith(']'):
                current_section = current_line[1:-1].strip()
                config[current_section] = {}
            # Process key-value pairs
            elif '=' in current_line:
                key, value = current_line.split('=', 1)
                key = key.strip()
                value = infer_type(value)
                if current_section:
                    config[current_section][key] = value
            else:
                # Handle invalid or unexpected lines if necessary
                pass
            current_line = ''
    return config

def main():
    parser = argparse.ArgumentParser(description='Convert a Splunk savedsearches.conf file to a YAML document.')
    parser.add_argument('filename', help='Path to the savedsearches.conf file')
    args = parser.parse_args()
    config = parse_savedsearches_conf(args.filename)

    # Create the 'output' directory if it doesn't exist
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    # Define the output YAML file path
    output_yaml_file = os.path.join(output_dir, 'output.yaml')

    # Write the YAML data to the output file
    with open(output_yaml_file, 'w') as f:
        yaml.dump(config, f, sort_keys=False)

    print(f"YAML output written to: {output_yaml_file}")

if __name__ == '__main__':
    main()
