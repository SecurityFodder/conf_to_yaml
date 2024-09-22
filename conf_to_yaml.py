import argparse
import yaml
import textwrap

def format_value(value):
    """Format the value for the .conf file, handling types and line continuations."""
    if isinstance(value, bool):
        return 'true' if value else 'false'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        return ','.join(str(item) for item in value)
    elif isinstance(value, str):
        # Split long strings into multiple lines with backslashes
        if len(value) > 80 or '\n' in value:
            lines = textwrap.wrap(value, width=80, break_long_words=False)
            formatted_value = ' \\\n    '.join(lines)
            return formatted_value
        else:
            return value
    else:
        # Default to string representation
        return str(value)

def convert_yaml_to_conf(yaml_filename, conf_filename):
    """Convert a YAML file back into a Splunk savedsearches.conf file."""
    with open(yaml_filename, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)

    with open(conf_filename, 'w') as conf_file:
        for section, options in data.items():
            conf_file.write(f'[{section}]\n')
            for key, value in options.items():
                formatted_value = format_value(value)
                conf_file.write(f'{key} = {formatted_value}\n')
            conf_file.write('\n')  # Add an empty line between sections

def main():
    parser = argparse.ArgumentParser(description='Convert a YAML file to a Splunk savedsearches.conf file.')
    parser.add_argument('yaml_filename', help='Path to the input YAML file')
    parser.add_argument('conf_filename', help='Path to the output savedsearches.conf file')
    args = parser.parse_args()
    convert_yaml_to_conf(args.yaml_filename, args.conf_filename)

if __name__ == '__main__':
    main()
